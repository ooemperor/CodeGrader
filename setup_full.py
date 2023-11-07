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
            'cgDeployDB = codeGrader.scripts.deployDB:main',
            'cgEvaluationService = codeGrader.scripts.cgEvaluationService:main',
            'cgExecutionService = codeGrader.scripts.cgExecutionService:main'
        ]
    }
)
