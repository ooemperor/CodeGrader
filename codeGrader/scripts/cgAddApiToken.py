"""
Script to generate an api token in the backend for the frontend.
Script will be generated and added to the server path.
@author: mkaiser
"""

from codeGrader.backend.db import Session, APIToken


def main(description):
    """
    Generate a API Token for the backend api, create the object in the database
    Return the token itself in a print statement
    @param description: The description for the token
    @type description: str
    @return: Authentication Token
    @rtype: str
    """

    sql = Session()  # open session
    api_token = APIToken(description=description)  # create the object
    token = api_token.token  # read the token from the object
    sql.create(api_token)  # write token to sql

    print(token)


if __name__ == '__main__':
    main("")
