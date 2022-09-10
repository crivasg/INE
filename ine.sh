#!/bin/sh

WORK_DIRECTORY=`basename "$0"`

cd ${WORK_DIRECTORY}

source venv/bin/activate
python -m ine
source venv/bin/deactivate
