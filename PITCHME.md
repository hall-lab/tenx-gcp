## Running De Novo Assemblies on the Cloud

Using Google deployments to run Supernova assemblies at scale using Cromwell workflows.

---

# 10X Supernova

Supernova is a software package for de novo assembly from Chromium Linked-Reads. These reads have an additional encoding that helps with creating diploid assemblies, representing maternal and paternal haplotypes.

---

# Challenges

* compute/storage resources
 * minimum compute resources are 32 cores and 256 GB
 * intermediate storage required is > 1TB
* scale to many assemblies
 * MGI produces 8+ at a time
* automate the assembly process
 * in-house code and a workflow system

---
# In House Code

Scripts and CLI to manage 10X resources and run the assembly pipeline. Also included Slack notification when pipelines start and finish.

---

# Cromwell

Cromwell is a Workflow Management System geared towards scientific workflows.

---

### Cromwell Workflow:

* download read fastqs
* assemble
* create output fastqs
* upload assembly to cloud storage

---

# Google Deployment Manager

Create and manage cloud resources with simple templates.

---

## Google DM Components

* YAML config
* Jinja template and schema
* Startup script

---

### Jinja Template and Schema

Jinja is a modern and designer-friendly templating language for Python, modelled after Django’s templates.

* Jinja file describes cloud resources
* Schema details the config properties

---

### Startup Script

Installs
* supernova
* cromwell
* in-house code
* additional Linux tools

---

### Config YAML

Includes the properties necaessrey to fconfigure the deployment

---

# LIVE DEMO

Fingers crossed :)

---

# FIN
