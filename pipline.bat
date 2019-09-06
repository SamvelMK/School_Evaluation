@ECHO OFF
ECHO Running The UNFPA E-Learning Module Pipeline.

ECHO Installing Python Modules.
pip freeze > requirements.txt
pip install -r requirements.txt --user
cls
ECHO Installation is complete.

cd %CD%\Scripts
ECHO Running the pipeline.

python -B master_script.py 
ECHO End of the pipline! You can check the log.txt file for more details.

PAUSE