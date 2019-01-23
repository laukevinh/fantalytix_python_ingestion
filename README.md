## About

RESTful API for crawling and representing professional sports statistics. 

---

## Setup

Clone repository and go to destination.
```
cd PATH_TO_DESTINATION/
```

Setup and activate virtual environment, normally same as destination.
```
virtualenv venv
source venv/bin/activate
```

Use pip to install setup, then install remaining requirements.txt
```
cd PATH_TO_DESTINATION/
pip install .
pip install -r requirements.txt
```

---

### Testing

To run all tests, go to the project root directory and run

`python -m unittest discover -v`

The project mostly uses absolute imports. However, the test files use relative 
imports because the test directory is not included in the package distribution.
