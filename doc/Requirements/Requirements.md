# Requirements
The requirements for the CodeGrader can be separated into two areas. 
- backend 
- frontend

All of the frontend requirements can be mapped to a backend requirement. 

The frontend requirements will be generalized and then transferred to the backend.

# Frontend

## Admin Site
The admin site will be accessible for all the AdminUsers.

### User Administration
- add a User
- remove a User
- update a User
  - change mail address
  - change password
- add User to Subjects
- remove User from Subjects
- see Submission Scores for a User
  - see all submissions for a User with the included scores. 

- 
### Subject Administration
- create Subject
- delete Subject
- Update Subject


- create exercise
- update exercise
- delete exercise
- add exercise to Subject
- remove exercise to Subject


- create Task
- update Task
- delete Task
- add Task to Exercise
- remove Task from Exercise

## User Site
- Login into user site
- see Subjects, Exercises and Tasks
- Download Task Description as file. 
- Upload solution to Task. 
- see result of Execution and Evaluation of the Task 

# Backend
The backend is made up of the following services, which each have individual requirements. 
- API Backend
- Execution Service
- Evaluation Service


## API Backend
The API Backend will be the only way to access the other Backend services. 

### Basic Objects.
For the following objects the basic requirements are the same
- User
- AdminUser
- Exercise
- Profile
- Subject
- Task

We need to be able to create, update, delete and get the following. Any special cases like adding a Task to a exercise can be done via the update operation. 

### File
- Upload a file via API
- Download a file via API

## Execution Service
- Execute a provided script in a sandbox and return the output of the executed file. 
  - output of the execution
  - status code of the execution
  - time used for the execution
  - memory used for the execution

## Evaluation Service
- evaluate the output from the execution Service
  - compare the output with a given example output
  - return if they match or if they do not match. 