from setuptools import setup, find_packages

PACKAGE_DATA = {
    "codeGrader.frontend.admin":[
        "/static/*.*",
        "/templates/*.*"
    ]
}

setup(
    name='codeGrader',
    version='1.0',
    packages=find_packages(exclude=["*backend*"]),
    url='https://github.com/ooemperor/CodeGrader',
    license='',
    author='mkaiser',
    author_email='',
    description='',
)
