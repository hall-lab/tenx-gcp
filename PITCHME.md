# Running De Novo Assemblies on the Cloud

Using Google deployments to run Supernova assemblies at scale using Cromwell workflows.

---

# 10X Supernova

Supernova is a software package for de novo assembly from Chromium Linked-Reads. These reads have an additional encoding that helps with creaating diploid assemblies, representing maternal and paternal haplotypes.

---

# Challenges

* compute/storage resources
 * minimum compute resources are 32 cores and 256 GB
 * intermediate storage required is > 1TB
* scale to many assemblies
 * MGI prodcues 8+ at a time
* automate the assembly process
 * in-house code and a workflow system

---

# Components

* cromwell
* google deployments

---

## Cromwell

Cromwell is a Workflow Management System geared towards scientific workflows.

Workflow:

* download read fastqs
* assemble
* create output fastqs
* upload assembly to cloud storage

---

## Google Deployment Manager

Create and manage cloud resources with simple templates.

---

## 

---
* 1
* 2

---
