from setuptools import setup, find_packages

PACKAGE_DATA = {
    "codeGrader.frontend": [
        "admin/static/*",
        "admin/static/*/*",
        "admin/static/*/*/*",
        "admin/templates/*.*"
    ]
}

setup(
    name='codeGrader',
    version='1.0',
    packages=find_packages(exclude=["*backend*"]),
    package_data=PACKAGE_DATA,
    url='https://github.com/ooemperor/CodeGrader',
    license='',
    author='mkaiser',
    author_email='',
    description='',
)
