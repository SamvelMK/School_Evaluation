#!/bin/sh

echo "Running UNFPA E_Learning Module Pipeline."

echo "Installing Python Modules."
pip3 install -r requirements.txt

echo "Installation is complete."

cd scripts
echo "Running the pipeline.";
python3 -B master_script.py 
echo "End of the pipline.";