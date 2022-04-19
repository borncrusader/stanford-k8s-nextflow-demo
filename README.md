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
   homepage. It's helpful to install this inside the cloned directory of this
   git repository.
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

## Steps
1. Ensure all dependencies are installed and start Docker Desktop (not required
   on Linux).
2. Start minikube server. You can confirm if minikube is running with the
   `minikube status` command.
```
$ minikube start
$ minikube status
minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

```
3. Clone the github repo and changed into the directory
```
$ git clone https://github.com/borncrusader/stanford-k8s-nextflow-demo
```
4. Make `data` directory mountable inside container. This command will not
   exit and will block. **This is only required if
   you're running MacOS or Windows.**
```
$ minikube mount $PWD/data:/data
```
5. Make sure you have installed Nexflow in the current directory. You should
   have a file called `nextflow` if you have done this.
6. In a new terminal window, you can start the nextflow process
```
./nextflow run ./nf/main.nf --in $PWD
```
7. This step should take 5-10 mins to run. Once it's done, you should see the
   prepared angles in a plot in the `data/` directory.

## Credits
1. This demo uses [MiniFold](https://github.com/hypnopump/MiniFold) and we're
   indebted to this project for making the scripts available.
2. We're hugely indebted to
   [proteinnet](https://github.com/aqlaboratory/proteinnet) for their amazing
   CASP7 database.
