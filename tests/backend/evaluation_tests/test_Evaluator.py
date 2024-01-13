# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

"""
Unit Tests for the Evaluation Classes.
@author: mkaiser
"""
import unittest
from codeGrader.backend.evaluation.Evaluation import Evaluation


class EvaluatorTest(unittest.TestCase):

    def setUp(self):
        """
        setUp which is run before every testcase specified in here
        @return: None
        """

        # setting up the evaluators
        self.basic = Evaluation('basic')
        self.lpl = Evaluation('line-per-line')
        self.lplBlank = Evaluation('line-per-line-ignore-blanks')

        # opening all the necessary files and writing the lines into arrays.
        f = open("./backend/evaluation_tests/solution_correct.txt", 'r')
        self.solutionFile = f.readlines()
        f.close()
        f = open("./backend/evaluation_tests/solution_with_blanks.txt", 'r')
        self.solutionFile_withBlanks = f.readlines()
        f.close()
        f = open("./backend/evaluation_tests/wrong_output.txt", 'r')
        self.errorOutput = f.readlines()
        f.close()

    def test_Evaluator_basic_1(self):
        """
        Test if the basic evaluator works with custom lists.
        @return: None
        """
        self.assertEqual('basic', self.basic.evaluation_type)
        self.assertTrue(self.basic.evaluate(["solution1"], ["solution1"]))
        self.assertFalse(self.basic.evaluate(["solution1"], ["solution2"]))

    def test_Evaluator_basic_2(self):
        """
        Test if the basic evaluator works with arrays read from a file
        @return: None
        """
        self.assertEqual('basic', self.basic.evaluation_type)
        self.assertTrue(self.basic.evaluate(self.solutionFile, self.solutionFile))
        self.assertFalse(self.basic.evaluate(self.solutionFile, self.errorOutput))

    def test_Evaluator_line_per_line(self):
        """
        Test if the line-per-line evaluator works with file input
        @return: None
        """
        self.assertEqual("line-per-line", self.lpl.evaluation_type)
        self.assertTrue(self.lpl.evaluate(self.solutionFile, self.solutionFile))
        self.assertFalse(self.lpl.evaluate(self.solutionFile, self.solutionFile_withBlanks))
        self.assertFalse(self.lpl.evaluate(self.solutionFile, self.errorOutput))

    def test_Evaluator_line_per_line_ignore_blanks(self):
        """
        Test if the line-per-line without blanks evaluator works with file input
        @return: None
        """
        self.assertEqual('line-per-line-ignore-blanks', self.lplBlank.evaluation_type)
        self.assertTrue(self.lplBlank.evaluate(self.solutionFile, self.solutionFile))
        self.assertTrue(self.lplBlank.evaluate(self.solutionFile, self.solutionFile_withBlanks))
        self.assertFalse(self.lplBlank.evaluate(self.solutionFile, self.errorOutput))
