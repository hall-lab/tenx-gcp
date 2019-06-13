# 10X Genomics Deployments and CLI

CLI, config, and resources for running 10X Genomics pipelines

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

## Configuring the Supernova Deployment for Google Cloud

### Edit the Supernova YAML Configuration File

Update these properties need to be set in the YAML (*resources/google/supernova.yaml*) configuration. Check _supernova.jinja.schema_ for supernova properties documentation.

#### Required Supernova Properties

| Property | Notes |
| --- | --- |
| service_account        | service account email to have authorized on the supernova VM |
| region/zone            | area to run instances, should match data location region/zone |
| remote_data_url        | bucket location of reads, software, and assemblies |
| supernova_software_url | supernova software TGZ URL (GS://) to download and untar |

#### Optional Supernova Properties

| Property | Notes |
| --- | --- |
| project_name      | project name label to add to instances |
| ssh_source_ranges | whitelist of IP ranges to allow SSH access to supernova compute instance |

### Create the Deployment

In an authenticated GCP session, enter the _resources/google_ directory. Run the command below to create the deployment named _supernova1_. The deployemnt name will be prepended to all assoiciated assets.
```
$ gcloud deploymewnt manager deployments create supernova1 --config supernova.yaml
```

### Start Supernova Pipeline

SSH into the supernova1 VM.
```
$ gcloud ssh supernova1
```
Then, run the supernova pipeline using the _tenx_ CLI providing a sample name. The pipeline expects reads to be in _${REMOTE_DATA_URL}/${SAMPLE_NAME}/reads_ and will put the resulting assembly and outputs into  _${REMOTE_DATA_URL}/${SAMPLE_NAME}/assembly_. This command redirects STDERR and STDOUT to a log file, and runs the command in the background. When running, supernova keeps a log in the assembly directory called _\_log_
```
[you@soupernova1 ~]$ tenx assembly pipeline ${SAMPLE_NAME} &> log &
```
Make sure to logout out of the session, and not let it exit happen because of timeout. Logout, exit or <CNTRL-D> your SSH session.
```
[you@soupernova1 ~]$ logout
```

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
