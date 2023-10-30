"""
Script File for starting the EvaluationService
@author: mkaiser
"""

import sys
from codeGrader.backend.evaluation import EvaluationRPC


def main():
    """
    Starting a new instance of the EvaluationService
    @return:
    """
    EvaluationRPC().start()


if __name__ == '__main__':
    sys.exit(main())
