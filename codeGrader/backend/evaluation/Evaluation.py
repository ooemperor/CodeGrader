"""
This is the Main File for the Evaluation Service, that compares the content of two files and returns a result.
@author: mkaiser
"""
from codeGrader.backend.db import Session


class Evaluation:
    """
    The Evaluator Class for the codeGrader
    """

    def __init__(self, evaluation_type: str):
        """
        Constructor for the Evaluator
        @param evaluation_type: The type of Evaluation that shall be used
        @type evaluation_type: str
        @return: The Evaluator object.
        @rtype: Evaluation
        """
        assert type is not None
        self.evaluation_type = evaluation_type
        self.sql_session = Session()  # needed so we can later expand the evaluations.

    def evaluate(self, expectedSolution, actualSolution):  # TODO: define data type of input
        """
        Evaluates the expected with the actualValue based
        First Basic Version that we need to further expand.
        @param expectedSolution: The expected solution from the task.
        @param actualSolution: The solution from the Exectuion Service
        @return: True if identical, else false
        @rtype: Boolean.
        """

        expectedSolution
        actualSolution
        assert actualSolution is not None
        assert self.evaluation_type is not None
        if self.evaluation_type == "basic":
            evaluation = self._basic_full_compare_evaluation(expectedSolution, actualSolution)
        elif self.evaluation_type == "line-per-line":
            evaluation = self._line_compare_evaluation(expectedSolution, actualSolution)
        elif self.evaluation_type == 'line-per-line-ignore-blanks':
            evaluation = self._line_compare_without_blanks_evaluation(expectedSolution, actualSolution)
        else:
            raise AttributeError("")
        return evaluation

    def _basic_full_compare_evaluation(self, expectedSolution: list, actualSolution: list):
        """
        Basic Fullcompare evaluation
        @param expectedSolution: The Solution that we expect to be correct. List of lines
        @type expectedSolution: list
        @param actualSolution: The solution that we got provided from the execution Service. List of lines
        @type actualSolution: list
        @return:
        """
        assert type(expectedSolution) == list
        assert type(actualSolution) == list
        assert self.evaluation_type == "basic"
        if expectedSolution == actualSolution:
            return True
        else:
            return False

    def _line_compare_evaluation(self, expectedSolution: list, actualSolution: list):
        """
        Function that compares
        @param expectedSolution: List of lines from the master solution from the Task.
        @type expectedSolution: list
        @param actualSolution: List of lines of the result from the execution Service
        @type actualSolution: list
        @return: True if all lines match.
        """
        assert self.evaluation_type == "line-per-line"
        assert expectedSolution is not None
        assert actualSolution is not None
        if len(expectedSolution) != len(actualSolution):
            # we do not have the same amount of output lines, so it does not match
            return False
        else:
            for i in range(0, len(expectedSolution)):
                if expectedSolution[i] == actualSolution[i]:
                    continue
                else:
                    return False  # lines do not match, we do not have the identical output
            return True

    def _line_compare_without_blanks_evaluation(self, expectedSolution: list, actualSolution: list):
        """
        Compare the two inputs while ignoring any additional blanks at the end of the line.
        @param expectedSolution: List of lines from the master solution from the Task.
        @type expectedSolution: list
        @param actualSolution: List of lines of the result from the execution Service
        @type actualSolution: list
        @return: True if all lines match.
        """
        assert self.evaluation_type == 'line-per-line-ignore-blanks'  # TODO: might wanna change this string to something better
        assert expectedSolution is not None
        assert actualSolution is not None

        if len(expectedSolution) > len(actualSolution):
            # we do not have the same amount of output lines, so it does not match
            return False

        else:
            j = 0  # counter for the expectedSolution
            for i in range(0, len(actualSolution)):
                if expectedSolution[i].strip() == actualSolution[i].strip():
                    continue
                else:
                    return False  # lines do not match, we do not have the identical output
            return True
