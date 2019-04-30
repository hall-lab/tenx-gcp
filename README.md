# 10X Genomics for GCP

Config, scripts and resources for running 10X Genomics pipelines in GCP

# Supernova

The 10X de novo assembler.

## Supernova Machine and Disk Requirements

| Property| Required | Recommended |
|---| --- | --- |
|Cores   | 32      | 64          |
|Mem     | 256+ Gb | 400+ Gb     |
|Disk    | 3 Tb    |2 Tb         |

GCP Machine recommended: n1-highmem-64

## Creating a Supernova Deployment

### Edit the supernova.yaml

Update these properties need to be set in the YAML (supernova.yaml) configuration.

| Required | Notes |
| --- | --- |
| service_account   | service account email to have authorized on the supernova VM |
| region/zone       | area to run instances, should match data location region/zone |
| remote_data_url   | bucket location of reads, software, and assemblies |
| supernova_version | supernova version to use, tgz must live at ${REMOTE_DATA_URL}/software/supernova-${SUPERNOVA_VERSION}.tgz |

| Optional | Notes |
| --- | --- |
| data_dir          | local working directory |
| project_name      | project name label to add to instances |
| ssh_source_ranges | IP ranges to restrict SSH access |

### Create the Deployment

### Start Supernova Pipeline

### Run Supernova Components Separately

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

# Cellranger

Not yet :(
