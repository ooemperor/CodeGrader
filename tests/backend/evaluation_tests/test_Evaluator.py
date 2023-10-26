import unittest
from codeGrader.backend.evaluation.Evaluation import Evaluation


class EvaluatorTest(unittest.TestCase):

    def setUp(self):
        """
        setUp which is run before every testcase specified in here
        @return: None
        """
        self.basic = Evaluation('basic')
        self.lpl = Evaluation('line-per-line')
        self.lplBlank = Evaluation('line-per-line-ignore-blanks')

        self.solutionFile = open("./backend/evaluation_tests/solution_correct.txt", 'rb')
        self.solutionFile_withBlanks = open("./backend/evaluation_tests/solution_with_blanks.txt", 'rb')

    def tearDown(self):
        """
        TearDown after each Test that is run.
        @return: None
        """
        self.solutionFile.close()
        self.solutionFile_withBlanks.close()

    def test_Evaluator_basic_1(self):
        self.assertEqual('basic', self.basic.evaluation_type)
        self.assertTrue(self.basic.evaluate("solution1", "solution1"))
        self.assertFalse(self.basic.evaluate("solution1", "solution2"))

    def test_Evaluator_basic_2(self):
        self.assertEqual('basic', self.basic.evaluation_type)
        self.assertTrue(self.basic.evaluate(self.solutionFile, self.solutionFile))

    def test_Evaluator_line_per_line(self):
        self.assertEqual(len(self.solutionFile.readlines()), len(self.solutionFile_withBlanks.readlines()))
        self.assertTrue(self.lpl.evaluate(self.solutionFile, self.solutionFile))

