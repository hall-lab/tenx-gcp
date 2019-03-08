# 10X Genomics for GCP

Config, scripts and resources for running 10X Genomics pipelines in GCP

# Longranger

The 10X aligner suite.

## Longranger Cluster Requirements

8-core Intel or AMD processor per node
6GB RAM per core
CentOS >=6
NFS w/ 2TB free disk space

# Loupe

View loupe files created by the longranger WGS pipeline.

## Loupe Requirements

Cores: 2
Mem:   8G+
Disk:  32G+ (loupe files are ~4G each)

# Supernova

The 10X de novo assembler.

## Supernova Requirements

Cores: 32
Mem:   256G+
Disk:  3T

# Cellranger

Not yet :(
