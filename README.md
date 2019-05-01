# 10X Genomics for GCP

Config, scripts and resources for running 10X Genomics pipelines in GCP

# Pipelines
[supernova](#supernova)  
[longranger](#longranger)  

<a name="supernova"/>

# Supernova

The 10X de novo assembler.

## Supernova Machine and Disk Requirements

| Property| Required | Recommended |
|---| --- | --- |
|Cores   | 32      | 64          |
|Mem     | 256+ Gb | 400+ Gb     |
|Disk    | 3 Tb    |2 Tb         |

GCP Machine recommended: n1-highmem-64

## Configuring the Supernova Deployment

### Edit the supernova.yaml

Update these properties need to be set in the YAML (*supernova.yaml*) configuration. Check _supernova.jinja.schema_ for supernova properties documentation.

#### Required Supernova Properties

| Property | Notes |
| --- | --- |
| cluster_name      | the prefix to all assests for the cluster (also deployment name) | 
| service_account   | service account email to have authorized on the supernova VM |
| region/zone       | area to run instances, should match data location region/zone |
| remote_data_url   | bucket location of reads, software, and assemblies |
| supernova_version | supernova version to use, tgz must live at ${REMOTE_DATA_URL}/software/supernova-${SUPERNOVA_VERSION}.tgz |

#### Optional Supernova Properties

| Property | Notes |
| --- | --- |
| data_dir          | local working directory |
| project_name      | project name label to add to instances |
| ssh_source_ranges | IP ranges to restrict SSH access |

### Create the Deployment

In an authenticated GCP session, create the deployment _supernova1_. For consistency, match the deployment name on the commandline with the cluster_name in the configuration YAML.
```
$ gcloud deploymewnt manager deployments  create supernova1 --config supernova.yaml
```

### Start Supernova Pipeline

SSH into the supernova1 VM, and run the supernova pipeline.
```
$ gcloud ssh supernova1
```
Then, run the supernova pipeline, providing a sample name. The pipeline expects reads to be in _${REMOTE_DATA_URL}/${SAMPLE_NAME}/reads_ and will put the resulting assembly and outputs into  _${REMOTE_DATA_URL}/${SAMPLE_NAME}/assembly_. This command redirects STDERR and STDOUT to a log file, and runs the command in the background. When running, supernova keeps a log in the assembly directory called _\_log_
```
[you@soupernova1 ~]$ run-supernova ${SAMPLE_NAME} &> log &
```
Make sure to logout out of the session, and not let itexit happen because of timeout.
```
[you@soupernova1 ~]$ logout
```

### Run Supernova and/or the Pipeline Components Separately

The supernova command itself plus the pipeline components can be run separately. Supernova is installed in /app/supernova and the pipeline scripts live in /apps/tenx-scripts.

<a name="longranger"/>

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
