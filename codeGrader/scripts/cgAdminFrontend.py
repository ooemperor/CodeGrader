"""
Script File for starting the Admin Frontend
@author: mkaiser
"""

import sys
from codeGrader.frontend.admin import admin_frontend


def main():
    """
    Starting a new instance of the EvaluationService
    @return:
    """
    admin_frontend()


if __name__ == '__main__':
    sys.exit(main())
