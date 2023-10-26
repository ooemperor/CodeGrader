from setuptools import setup, find_packages

setup(
    name='codeGrader',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/ooemperor/CodeGrader',
    license='',
    author='mkaiser',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'codeGraderDeployDB = codeGrader.scripts.deployDB:main'
        ]
    }
)
