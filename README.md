# Description

The awesome project to work on something

# Run It

`TODO: clean up and document properly`

```
../venv3/bin/cookiecutter --no-input -o ../ .

cd <prj_path>
make venv_install_requirements
git init
source .venv3/bin/activate
pre-commit install

git add .
git commit -am 'initial commit'

make start_local
make logs

make clean_all

make restart_local
make stop_local
```
