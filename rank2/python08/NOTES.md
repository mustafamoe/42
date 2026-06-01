
# Install from requirements file
python3 -m pip install -r requirements.txt

# venv stuff
python3 -m venv (name of vrital env e.g. "matrix_env")
source matrix_env/bin/activate # to activate the venv
deactivate
rm -rf matrix_env # to 

# ex1 mypy run
python3 -m pip install mypy
pthon3 -m mypy loading.py