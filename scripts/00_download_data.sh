#!/bin/bash

set -e

cd data

echo "Downloading CASP7 data from proteinnet"

wget -O data/casp7.tar.gz \
    https://sharehost.hms.harvard.edu/sysbio/alquraishi/proteinnet/human_readable/casp7.tar.gz

echo "Extracting archive"
tar xfz casp7.tar.gz
