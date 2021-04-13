# pg_demonic
Pg tool for operation and management
## Configure script (dev)
```bash
pip3 install setuptools --upgrade
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```
## Compile to one binary
```bash
pyinstaller --onefile pg.py
# binary location = dist/pg
```
