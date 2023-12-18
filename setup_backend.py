from setuptools import setup, find_packages

setup(
    name='codeGrader',
    version='1.0',
    packages=find_packages(exclude=["*frontend*"]),
    url='https://github.com/ooemperor/CodeGrader',
    license='',
    author='mkaiser',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'cgDeployDB = codeGrader.scripts.deployDB:main',
            'cgEvaluationService = codeGrader.scripts.cgEvaluationService:main',
            'cgExecutionService = codeGrader.scripts.cgExecutionService:main',
            'cgAddApiToken = codeGrader.scripts.cgAddApiToken:main',
            'cgApiBackend = codeGrader.scripts.cgApiBackend:main'

        ]
    }
)
