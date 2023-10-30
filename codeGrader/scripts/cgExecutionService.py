"""
Script File for starting the ExecutionService
@author: mkaiser
"""

import sys
from codeGrader.backend.execution import ExecutionRPC


def main():
    """
    Starting a new instance of the ExecutionService
    @return:
    """
    ExecutionRPC().start()


if __name__ == '__main__':
    sys.exit(main())
