
[![Build Status](https://travis-ci.org/hall-lab/tenx-gcp.svg?branch=master)](https://travis-ci.org/hall-lab/tenx-gcp)

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
| project_name      | project name label to add to instances, useful for accounting |
| node_count        | number of compute instances to spin up. It is recommended to only run one supernova assemble per instance |
| notification      | slack url to post message (see making a slack app) |
| ssh_source_ranges | whitelist of IP ranges to allow SSH access to supernova compute instance |

### Create the Deployment

In an authenticated GCP session, enter the _resources/google_ directory. Run the command below to create the deployment named _supernova1_. The deployment name will be prepended to all assoiciated assets. Use a different deployment name as needed.
```
$ gcloud deployment-manager deployments create supernova01 --config supernova.yaml
```

### Assests Created

This is list of assets created in the deployment. All assests are preppended with the **deployment name** and a '-'. The compute instances with have a number appended to them. The number of compute instances depends on the *node_count* in the deployment YAML. It is recommended to only run one supernova assembly per compute instance.

| Assest | Name | Purpose |
| --- | --- | --- |
| supernova01-1 (to node_count)           | compute.v1.instance   | the supernova compute instances, run supernova here |
| supernova01-network                     | compute.v1.network    | network for compute instance and firewalls |
| supernova01-network-subnet              | compute.v1.subnetwork | subnet for compute instance and firewalls |
| supernova01-network-tenx-ssh-restricted | compute.v1.firewall   | firewall of whitelisted IPS for SSH |
| supernova01-network-tenx-web-ui         | compute.v1.firewall   | firewall to allow access to the 10X web UI |

### Start Supernova Pipeline

SSH into the supernova01-1 compute instance.
```
$ gcloud compute ssh supernova01-1
```
Then, run the supernova pipeline using the _tenx_ CLI providing a sample name. The pipeline expects reads to be in _${REMOTE_DATA_URL}/${SAMPLE_NAME}/reads_ and will put the resulting assembly and outputs into  _${REMOTE_DATA_URL}/${SAMPLE_NAME}/assembly_. This command redirects STDERR and STDOUT to a log file, and runs the command in the background. When running, supernova keeps a log in the assembly directory called _\_log_
```
[you@soupernova01-1 ~]$ tenx asm pipeline ${SAMPLE_NAME} &> log &
```
Make sure to logout out of the session, and not let it exit happen because of timeout. Logout, exit or <CNTRL-D> your SSH session.
```
[you@soupernova01-1 ~]$ logout
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
