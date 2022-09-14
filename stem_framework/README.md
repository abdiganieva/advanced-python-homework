# STEM framework

STEM framework is a framework I don't know yet what is for.

## Development installation
We use `conda` from [Anaconda](https://www.anaconda.com/products/distribution) for package and development environment management.



Create a virtual environment (if you wish) by running
```
conda env create -f conda-env.yml 
```
To activate this environment, use
```
conda activate stem-framework-dev
```

Install this project in editable mode 
```
cd ./stem_framework
pip install -e .
```
## Building docs

Building docs is managed via Sphinx
```
cd ./docs
make html
```
Sphinx will build HTML files.

Alternatively it's allowed to build documentation using
```
python setup.py build_sphinx
```
