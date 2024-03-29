# mtDNA Analysis Tool

This repository contains a Python script for analysing mitochondrial DNA (mtDNA) variants according to: MITOMAP, HelixMTdb, gnomAD and MitImpact 3D. The script performs several steps including data merging, filtering and mapping of variants to loci. This script has been created to filter files from mtDNA-Server.

# Overview

This Python script is designed to perform the following tasks:

1. Identify confirmed pathogenic variants using the MITOMAP database.
2. Find zero frequency variants using the HelixMTdb database.
3. Find zero frequency variants using the gnomAD database.
4. Match zero frequency variants with predictions using the MitImpact database.
5. Map variant positions to mtDNA loci.

# Installation

1. Clone the repository to your local machine:

```bash
https://github.com/skoczylass/mtDNA_analysis.git
```
1. Make sure you have Python 3.11 installed.

2. Install the necessary Python libraries:

```bash
pip install pandas
```

## Running with Docker (Linux or Windows)

If you prefer to run the script using Docker on your system, follow these steps:

1. Install Docker Desktop for Windows from here if you haven't already.

2. Open PowerShell or Linux Terminal.

3. Pull the Docker image from Docker Hub:
   
```bash
docker pull tomlodz1/mtdnav1:latest
```

3. Navigate to the directory containing your input data and where you want to store the results. 

4. Run the Docker container, mounting the Input and Results directories:
   
```bash
docker run -v "Path\Input:/Input" -v "Path\Results:/Results" tomlodz1/mtdnav1:latest
```

or

```bash
sudo docker run -v "${PWD}/path:"/Results" -v "${PWD}/path":"/Input" mtdnav1
```

The script will run inside the Docker container and the results will be generated in the Results directory.

## Additional step
Ensure that any necessary input files are included in the Input directory, and that databases are stored in the Database directory.
