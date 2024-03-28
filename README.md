# mtDNA Analysis Tool

This repository contains a Python script for analyzing mitochondrial DNA (mtDNA) variants using various databases. The script performs several steps including data merging, filtering, and mapping of variants to loci.

## Overview

The provided Python script is designed to perform the following tasks:

1. Identify confirmed pathogenic variants using MITOMAP database.
2. Analyze variants with zero frequency in HelixMTdb database.
3. Match variants with predictions using MitImpact database.
4. Compare variants with gnomAD database.
6. Map variant positions to loci.

## Installation
## Running with Docker Linux or Windows

1. Install Docker Desktop for Windows from [here](https://www.docker.com/products/docker-desktop).

2. Open PowerShell or Command Prompt.

3. Pull the Docker image from Docker Hub:

```bash
docker pull tomlodz1/mtdnav1:latest

docker run -v "C:\mtDNA_analysis\Input:/Input" -v "C:\mtDNA_analysis\Results:/Results" tomlodz1/mtdnav1:latest

Or
1. Clone the repository to your local machine:

```bash
git clone https://github.com/YourUsername/mtDNA_analysis.git


### Additional Steps
1. Ensure that all necessary input files are included in the `Input` directory, and databases are stored in the `Database` directory.
