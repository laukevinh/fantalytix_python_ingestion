"""Put this 'setup.py' file on the same level as the packages you want to import

MyProject
│
├── src
│   │
│   └── myproject
│       │
│       ├── module_A
│       │   │
│       │   ├── file.py
│       │   └── __init__.py
│       │
│       ├── module_B
│       │   │
│       │   ├── file.py
│       │   └── __init__.py
│       │
│       └── __init__.py
│
├── test
│   │
│   ├── module_A
│   │   ├── file.py
│   │   └── __init__.py
│   │
│   ├── module_B
│   │   ├── file.py
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── setup.py
└── venv
    ├── Include
    ├── Lib
    ├── pyvenv.cfg
    └── Scripts [87 entries exceeds filelimit, not opening dir]

Use the following commands

$ cd MyProject/
$ source venv/bin/activate
$ pip install .

To use in a package

>>> from myproject.modeul_A import file

To uninstall, pip uninstall and delete the .egg folder.

$ pip uninstall MyProject

More at https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
"""

from setuptools import setup, find_packages
setup(
    name='FantalytixPythonIngestion', 
    version='1.0', 
    packages=find_packages("src"),
    package_dir={"":"src"},
)
