# Backend Handlers
The handlers in the backend are found in the <code>src.backend.handlers</code> package.
Each handler has its own basic functionalities. 

We could easily write a single function to handle all the get functions for all the Elements, but we do not want that. 
Since we will later wanna introduce the multi-client-capabilty, we will need the custom handlers, since each Object can have differences in the get Functions. 
Each "simple" Object has at least a get and post function. 

## Operations:
### get
Just a get Operation which returns a json representation of an object out of the database

### post
POST Creates new objects/entries in the database

### put
PUT is used to update an object/entry in the database