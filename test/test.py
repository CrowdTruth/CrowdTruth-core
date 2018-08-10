import unittest

import crowdtruth
from crowdtruth.configuration import DefaultConfig
import logging
import string


class TestConfig(DefaultConfig):
	inputColumns = ["in_col"]
	outputColumns = ["out_col"]
	open_ended_task = False
	annotation_separator = " "
	annotation_vector = list(string.ascii_uppercase)
	def processJudgments(self, judgments):
		return(judgments)
test_conf_const = TestConfig()

test_config = test_conf_const.__class__
data, config = crowdtruth.load(file = "10work_disagr.csv", config = test_config())
results = crowdtruth.run(data, config)

class TestAgreement(unittest.TestCase):

	def test_all_workers_agree(self):
		for w in range(2,11):
			test_config = test_conf_const.__class__
			data, config = crowdtruth.load(
				file = str(w) + "work_agr.csv",
				config = test_config())
			results = crowdtruth.run(data, config)
			self.assertAlmostEqual(results["units"]["uqs"].at[1], 1.0)
			for wid in range(w):
				self.assertAlmostEqual(results["workers"]["wqs"].at["W" + str(wid + 1)], 1.0)
			self.assertAlmostEqual(results["annotations"]["aqs"]["A"], 1.0)

	def test_all_workers_disagree(self):
		for w in range(2,11):
			test_config = test_conf_const.__class__
			data, config = crowdtruth.load(
				file = str(w) + "work_disagr.csv",
				config = test_config())
			results = crowdtruth.run(data, config)
			self.assertAlmostEqual(results["units"]["uqs"].at[1], 0.0)
			for wid in range(w):
				self.assertAlmostEqual(results["workers"]["wqs"].at["W" + str(wid + 1)], 0.0)
				self.assertAlmostEqual(results["annotations"]["aqs"][list(string.ascii_uppercase)[w]], 0.0)

	# def test_all_workers_disagree(self):
	# self.assertTrue()


if __name__ == '__main__':
    unittest.main()