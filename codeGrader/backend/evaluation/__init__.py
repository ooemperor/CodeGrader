"""
This package is used for the evaluation service of the CodeGrader
@author: mkaiser
"""

from .EvaluationRPC import EvaluationRPC
from .Evaluation import Evaluation

__all__ = ["EvaluationRPC", "Evaluation"]
