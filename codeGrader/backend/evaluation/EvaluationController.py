"""
Controller for the evaluation objects.
@author: mkaiser
"""

from codeGrader.backend.db import Session, Submission, EvaluationResult
from codeGrader.backend.evaluation.Evaluation import Evaluation


class EvaluationController:
    """
    A Custom Controller to evaluate the result of all the TestCases for a given Submission/Task
    Runs an evaluation for every TestCase/ExecutionResult that we have
    """

    def __init__(self, submission_id: int) -> None:
        """
        The constructor for the Controller
        """
        self.sql_session = Session()

        self.submission = self.sql_session.get_object(Submission, submission_id)

        self.testcases = self.submission.TaskSubmission.testcases
        self.testcases_count = len(self.testcases)
        self.execution_results = self.submission.executionresult

        # next lines would fail if the amount of testcases does not equal the amount of execution results
        assert self.testcases is not None
        assert self.testcases_count is not None and self.testcases_count >= 0
        assert self.execution_results is not None
        assert self.testcases_count == len(self.execution_results)

        self.evaluation = Evaluation("basic")

    def evaluate(self) -> None:
        """
        Starts the evaluation for each TestCase/ExecutionResult
        @return:
        """
        evaluation_counter = 0
        evaluation_successful_counter = 0
        for testcase in self.testcases:
            for execution_result in self.execution_results:

                if testcase.id == execution_result.testcase_id:

                    # preparing the outputs to a list or the evaluation.
                    expected_list = self._prepareFileContent(
                        str(testcase.output_file.getFileContent().tobytes().decode('UTF-8')))
                    actual_list = self._prepareFileContent(execution_result.execution_output)

                    # evaluation returns True if they match.
                    if self.evaluation.evaluate(expected_list, actual_list):
                        evaluation_successful_counter += 1
                    evaluation_counter += 1

                else:
                    continue

        assert evaluation_counter == self.testcases_count
        assert evaluation_counter >= evaluation_successful_counter

        score: float = evaluation_successful_counter / evaluation_counter
        self._addEvaluationResult(score)

    @staticmethod
    def _prepareFileContent(file_content: str) -> str:
        """
        Preparing the given File Content into a list of lines.
        @param file_content: The content of a file to be prepared
        @type file_content: str
        @return: The list of lines in the file_content
        @rtype: list
        """
        assert file_content is not None
        return file_content.splitlines(False)

    def _addEvaluationResult(self, score: float) -> None:
        """
        Adding an EvaluationResult to the database.
        @param score: The score of the evaluation
        @type score: float
        @return: Nothing
        @rtype: None
        """
        data = dict()
        data["evaluation_score"] = score
        data["submission_id"] = self.submission.id

        exec_result = EvaluationResult(**data)

        Session().create(exec_result)
