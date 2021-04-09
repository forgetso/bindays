#!/bin/bash
source /opt/conda/etc/profile.d/conda.sh
conda activate $CONDAENV;
cd /bindays/backend;
echo $(ls);
exec waitress-serve --port=5000 api:app;
