"""
Script File for starting the API in the backend
@author: mkaiser
"""

import sys
from codeGrader.backend.api.app import api_backend


def main():
    """
    Starting a new instance of the EvaluationService
    @return:
    """
    api_backend()


if __name__ == '__main__':
    sys.exit(main())
