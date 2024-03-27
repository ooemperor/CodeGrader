# Backend Documentation

Within this fodler you will find the documentation for the backend. 

## API
The API provides the main Functionality and implements the access via REST API to the Data in the Database. 
It is implemented using Python and Flask. 

## Database
The Database used in testing is PostgreSQL. The Datamodel is automatically created with SQLAlchemy. 

## Execution Service
The Execution Service executes a Script in a secured environment using LXC. The controller for the LXC is also written in Python.

## Evaluation Service
After the execution has finished the Evaluation Service compares the expected output of the Submission with the correct output defined by the uploaded Solution. 