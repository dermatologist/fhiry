* pip install pip-tools

* pip-compile --upgrade
* pip-compile dev-requirements.in

* pip-sync

OR

* pip-sync requirements.txt dev-requirements.txt


## pre-commit

* pip install pre-commit

* pre-commit install

## uv

* pip install uv
* uv pip compile setup.cfg -o requirements.txt --universal
* uv pip compile dev-requirements.in -o dev-requirements.txt --universal