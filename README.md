# mtDNA Analysis Tool

This repository contains a Python script for analyzing mitochondrial DNA (mtDNA) variants using various databases. The script performs several steps including data merging, filtering, and mapping of variants to loci.

## Overview

The provided Python script is designed to perform the following tasks:

1. Identify confirmed pathogenic variants using MITOMAP database.
2. Analyze variants with zero frequency in HelixMTdb database.
3. Match variants with predictions using MitImpact database.
4. Compare variants with gnomAD database.
5. Map variant positions to loci.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/YourUsername/mtDNA_analysis.git
```

1. Ensure you have Python installed. You can download it from here.
2. Install the required Python libraries:

pip install pandas

Certainly! Here's a revised version of your README.md with the requested changes and some additional details:

markdown

# mtDNA Analysis Tool

This repository contains a Python script for analyzing mitochondrial DNA (mtDNA) variants using various databases. The script performs several steps including data merging, filtering, and mapping of variants to loci.

## Overview

The provided Python script is designed to perform the following tasks:

1. Identify confirmed pathogenic variants using MITOMAP database.
2. Analyze variants with zero frequency in HelixMTdb database.
3. Match variants with predictions using MitImpact database.
4. Compare variants with gnomAD database.
5. Map variant positions to loci.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/YourUsername/mtDNA_analysis.git

    Ensure you have Python installed. You can download it from here.

    Install the required Python libraries:

bash

pip install pandas

Running with Docker (Linux or Windows)

If you prefer to run the script using Docker on your system, follow these steps:

1. Install Docker Desktop for Windows from here if you haven't already.

2. Open PowerShell or Command Prompt.

3. Pull the Docker image from Docker Hub:

docker pull tomlodz1/mtdnav1:latest

1. Navigate to the directory containing your input data and where you want to store the results. Let's assume it's the C:\mtDNA_analysis directory for Windows.

2. Run the Docker container, mounting the Input and Results directories:

docker run -v "C:\mtDNA_analysis\Input:/Input" -v "C:\mtDNA_analysis\Results:/Results" tomlodz1/mtdnav1:latest

1. The script will run inside the Docker container, and the results will be generated in the Results directory.

Additional Steps

1. Ensure that all necessary input files are included in the Input directory, and databases are stored in the Database directory.

2. Update the input files as needed before running the script.

3. Customize any parameters or settings directly in the script according to your analysis requirements.

4. After running the script, review the results in the Results directory. You may need to interpret or further analyze the generated files based on your specific research goals.
