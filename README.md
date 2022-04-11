## About
This demo uses [MiniFold](https://github.com/hypnopump/MiniFold) to demonstrate
a protein structure prediction (also known as Protein Folding) from a sequence
of polypeptides.

## Necessities
To successfully run this demo, you will need to install the following software
on your machine. All these are available on Windows, macOS and Linux.

1. [Docker](https://docs.docker.com/desktop/)
2. [Nextflow](https://www.nextflow.io/)
3. [Minikube](https://minikube.sigs.k8s.io/docs/start/)

You don't have to be a master of the command line but you should know how to
use a command line and run some simple commands.

You will also need to have a login with [github.com](https://github.com) which
likely you have already.

## Installation
1. Install [Docker Desktop](https://docs.docker.com/desktop/) on your platform.
   If you're using Linux, you might want to install docker from your distro's
   package registry instead of installing Docker Desktop.
2. Install [Nextflow](https://www.nextflow.io) following the steps in their
   homepage.
3. Install [Minikube](https://minikube.sigs.k8s.io/docs/start/) following the
   link.
4. Follow the steps [here](https://minikube.sigs.k8s.io/docs/drivers/docker/)
   to choose docker as your default driver for minikube and run the minikube
   cluster. This might take a while if you're running this for the first time
   since this would have to download the base image for your minikube cluster.

## Data Preparation
The demo utilizes data from the venerable
[proteinnet](https://github.com/aqlaboratory/proteinnet) database. We'll be
using the
[CASP7](https://sharehost.hms.harvard.edu/sysbio/alquraishi/proteinnet/human_readable/casp7.tar.gz)
test data for our demo. Please download this archive and uncompress the
`.tar.gz` file in the `data/` directory. Alternatively, you can use the
[scripts/00_download_data.sh](scripts/00_download_data.sh) to download and
extract this data for you from the command line like so

```
$ bash scripts/00_download_data.sh
```

## Nextflow
### Steps


## Minikube
### Steps

## Credits
1. This demo uses [MiniFold](https://github.com/hypnopump/MiniFold) and we're
   indebted to this project for making the scripts available.
2. We're hugely indebted to
   [proteinnet](https://github.com/aqlaboratory/proteinnet) for their amazing
   CASP7 database.
