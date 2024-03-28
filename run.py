import pandas as pd
import os

# Funkcja do scalania ramek danych
def merge_dataframes(df1, df2):
    merged_df = pd.merge(df1, df2, on="Pos_ref_alt", how="inner")
    return merged_df

# Funkcja do znalezienia unikalnych i powtarzających się wierszy
def find_unique_duplicates(df1, df2):
    non_matching_df_unique = df1[~df1["Pos_ref_alt"].isin(df2["Pos_ref_alt"])].copy()
    non_matching_df_unique.drop_duplicates(subset="Pos_ref_alt", keep=False, inplace=True)

    non_matching_df_multi = df1[~df1["Pos_ref_alt"].isin(df2["Pos_ref_alt"])].copy()
    non_matching_df_multi = non_matching_df_multi[non_matching_df_multi["Pos_ref_alt"].duplicated(keep=False)]

    return non_matching_df_unique, non_matching_df_multi

# Funkcja do zapisu danych do pliku tekstowego
def write_to_text(dataframe, text_path, comment=None):
    if comment:
        with open(text_path, 'w') as file:
            file.write(f"# {comment}\n")
    dataframe.to_csv(text_path, sep='\t', index=False, mode='a', header=not os.path.exists(text_path))

# Funkcja do mapowania pozycji na locus
def map_position_to_locus(position, loci_df):
    for index, row in loci_df.iterrows():
        if row['Starting'] <= position <= row['Ending']:
            return f"{row['Map Locus']}\t{row['Description']}"
    return "Unknown\tUnknown"

# Funkcja do dodawania zmapowanych danych
def add_mapped_data(file_path, loci_df):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    mapped_lines = []
    for line in lines:
        if line.startswith("Pos_ref_alt"):
            mapped_lines.append(f"{line.strip()}\tMapped Map Locus\tMapped Description")
        else:
            pos_ref_alt = line.split("\t")[0]
            mapped_data = map_position_to_locus(int(pos_ref_alt.split(":")[0]), loci_df)
            mapped_lines.append(f"{line.strip()}\t{mapped_data}")

    with open(file_path, 'w') as output_file:
        output_file.write('\n'.join(mapped_lines))

# Pozostałe funkcje i definicje stałych

# Definitions of constants
BASE_DIR = r"C:\Users\sebas\OneDrive\Dokumenty\mtDNA_WES\Kod\mtDNA_analysis_mtDNAServer"
INPUT_DIR = os.path.join(BASE_DIR, "Input")
RESULTS_DIR = os.path.join(BASE_DIR, "Results")
DATABASES_DIR = os.path.join(BASE_DIR, "Database")

# Make sure the Results directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Additional Step: Remove existing files in the Results directory
existing_files = os.listdir(RESULTS_DIR)
for file in existing_files:
    file_path = os.path.join(RESULTS_DIR, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

# Step 0: Sort variants.txt by "Pos" in descending order
input_txt_path = os.path.join(INPUT_DIR, "variants.txt")
df_variants = pd.read_csv(input_txt_path, sep='\t')
df_variants = df_variants.sort_values(by='Pos', ascending=True)  # Change to ascending order
df_variants.to_csv(input_txt_path, sep='\t', index=False)

# Step 1
output_text_path_step_1 = os.path.join(RESULTS_DIR, "Step_1.txt")
df_step_1 = df_variants[["Pos", "Ref", "Variant", "SampleID", "Variant-Level", "Coverage-Total"]].copy()
df_step_1['Pos_ref_alt'] = df_step_1.apply(lambda row: f"{row['Pos']}:{row['Ref']}:{row['Variant']}", axis=1)
df_step_1 = df_step_1[["Pos_ref_alt", "SampleID", "Variant-Level", "Coverage-Total"]]
write_to_text(df_step_1, output_text_path_step_1)

# Step 2
df_mitomap = pd.read_csv(os.path.join(DATABASES_DIR, "MITOMAP.txt"), sep='\t')
output_text_path_step_2 = os.path.join(RESULTS_DIR, "Confirmed Pathogenic Variants.txt")
merged_df_step_2 = merge_dataframes(df_step_1, df_mitomap)

if merged_df_step_2.empty:
    with open(output_text_path_step_2, 'w') as file:
        file.write("No confirmed pathogenic or likely pathogenic variant found.")
else:
    write_to_text(merged_df_step_2, output_text_path_step_2)

# Step 3
df_helix = pd.read_csv(os.path.join(DATABASES_DIR, "HelixMTdb.txt"), sep='\t')
output_path_step_3 = os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Repeats.txt")
merged_df_step_3 = merge_dataframes(df_step_1, df_helix)
non_matching_df_unique_step_3, non_matching_df_multi_step_3 = find_unique_duplicates(df_step_1, df_helix)

# Add Frequency column
non_matching_df_multi_step_3['Frequency'] = non_matching_df_multi_step_3.groupby('Pos_ref_alt')['Pos_ref_alt'].transform('count')

# Sort by Frequency
non_matching_df_multi_step_3 = non_matching_df_multi_step_3.sort_values(by='Frequency', ascending=True)

write_to_text(non_matching_df_unique_step_3, os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Unique.txt"))
write_to_text(non_matching_df_multi_step_3, output_path_step_3)

# Step 3.5: Merge HelixMTdb data with df_step_1
df_helix = pd.read_csv(os.path.join(DATABASES_DIR, "HelixMTdb.txt"), sep='\t')
merged_df_step_3_5 = merge_dataframes(df_step_1, df_helix)

# Create a new file containing only matched variants where df_step_1 is common for both dataframes
output_path_step_3_5 = os.path.join(RESULTS_DIR, "Matched Variants in HelixMTdb.txt")

if not merged_df_step_3_5.empty:
    write_to_text(merged_df_step_3_5, output_path_step_3_5)
else:
    with open(output_path_step_3_5, 'w') as file:
        file.write("No matched variants found in HelixMTdb.")

# Step 4
df_non_matching_step_3 = pd.read_csv(os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Repeats.txt"), sep='\t')
df_mitimpact = pd.read_csv(os.path.join(DATABASES_DIR, "MitImpact_db_3.1.0.txt"), sep='\t', low_memory=False)
output_text_path_step_4 = os.path.join(RESULTS_DIR, "Matched Variants Prediction.txt")
merged_df_step_4 = merge_dataframes(df_non_matching_step_3, df_mitimpact)
matched_df_step_4 = merged_df_step_4[merged_df_step_4['Gene_symbol'].notnull()]

write_to_text(matched_df_step_4, output_text_path_step_4, comment="No prediction found")

# Step 5.1: Compare Step_1.txt with gnomad.txt
df_gnomad = pd.read_csv(os.path.join(DATABASES_DIR, "gnomad.txt"), sep='\t')

# Merge Step_1.txt with gnomad.txt based on Pos_ref_alt
merged_df_step_5_1 = merge_dataframes(df_step_1, df_gnomad)

# Identify non-matching rows (Step_1.txt entries not present in gnomad.txt)
non_matching_df_step_5_1 = df_step_1[~df_step_1["Pos_ref_alt"].isin(df_gnomad["Pos_ref_alt"])].copy()

# Save non-matching entries to "Zero Frequency in gnomad_Unique.txt"
output_path_step_5_1_zero_frequency_unique = os.path.join(RESULTS_DIR, "Zero Frequency in gnomAD_Unique.txt")
non_matching_df_step_5_1_unique = non_matching_df_step_5_1[~non_matching_df_step_5_1["Pos_ref_alt"].duplicated(keep=False)].copy()
write_to_text(non_matching_df_step_5_1_unique, output_path_step_5_1_zero_frequency_unique)

# Save repeated non-matching entries to "Zero Frequency in gnomad_Repeats.txt"
output_path_step_5_1_zero_frequency_repeats = os.path.join(RESULTS_DIR, "Zero Frequency in gnomAD_Repeats.txt")
non_matching_df_step_5_1_repeats = non_matching_df_step_5_1[non_matching_df_step_5_1["Pos_ref_alt"].duplicated(keep=False)].copy()
write_to_text(non_matching_df_step_5_1_repeats, output_path_step_5_1_zero_frequency_repeats)

# Save matching entries to "Matched Variants in gnomad.txt"
output_path_step_5_1_matched_variants = os.path.join(RESULTS_DIR, "Matched Variants in gnomAD.txt")
if not merged_df_step_5_1.empty:
    write_to_text(merged_df_step_5_1, output_path_step_5_1_matched_variants)
else:
    with open(output_path_step_5_1_matched_variants, 'w') as file:
        file.write("No matched variants found in gnomAD.")

# Step 5.2: Create a combined file with information from Step_1.txt and gnomad.txt
combined_df_step_5_2 = pd.concat([merged_df_step_5_1, non_matching_df_step_5_1])

# Load data from "Loci.txt" file
loci_df = pd.read_csv(os.path.join(DATABASES_DIR, "Loci.txt"), delimiter="\t")

# Step 6
output_path_step_5_unique = os.path.join(RESULTS_DIR, "Mapped Variants with a frequency of zero in HelixMTdb_Unique.txt")
output_path_step_5_repeats = os.path.join(RESULTS_DIR, "Mapped Variants with a frequency of zero in HelixMTdb_Repeats.txt")
output_path_step_5_unique = os.path.join(RESULTS_DIR, "Zero Frequency in gnomAD_Unique.txt")
output_path_step_5_repeats = os.path.join(RESULTS_DIR, "Zero Frequency in gnomAD_Repeats.txt")

add_mapped_data(os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Unique.txt"), loci_df)
add_mapped_data(os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Repeats.txt"), loci_df)
add_mapped_data(os.path.join(RESULTS_DIR, "Zero Frequency in gnomAD_Unique.txt"), loci_df)
add_mapped_data(os.path.join(RESULTS_DIR, "Zero Frequency in gnomAD_Repeats.txt"), loci_df)

# Remove Step_1.txt
os.remove(output_text_path_step_1)

# Additional Step: Remove temporary files if needed
# Uncomment the following lines if you want to remove temporary files created in previous steps
# os.remove(os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Unique.txt"))
# os.remove(os.path.join(RESULTS_DIR, "Variants with a frequency of zero in HelixMTdb_Repeats.txt"))