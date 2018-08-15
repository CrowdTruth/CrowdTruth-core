
import unittest
import string
# import logging

import crowdtruth
from crowdtruth.configuration import DefaultConfig

class TestConfigOpen(DefaultConfig):
    inputColumns = ["in_col"]
    outputColumns = ["out_col"]
    open_ended_task = True
    annotation_vector = list(string.ascii_uppercase)
    def processJudgments(self, judgments):
        return(judgments)

class TestConfigClosed(DefaultConfig):
    inputColumns = ["in_col"]
    outputColumns = ["out_col"]
    open_ended_task = False
    annotation_separator = " "
    annotation_vector = list(string.ascii_uppercase)
    def processJudgments(self, judgments):
        return(judgments)

# test_conf_const = TestConfigOpen()
# test_config = test_conf_const.__class__
# data, config = crowdtruth.load(file = "4work_outlier.csv", config = test_config())
# results = crowdtruth.run(data, config)

class TestAgreementClosed(unittest.TestCase):
    test_conf_const = TestConfigClosed()

    def test_all_workers_agree(self):
        for w in range(2,11):
            test_config = self.test_conf_const.__class__
            data, config = crowdtruth.load(
                file = "test/" + str(w) + "work_agr.csv",
                config = test_config())
            results = crowdtruth.run(data, config)
            self.assertAlmostEqual(results["units"]["uqs"].at[1], 1.0)
            for wid in range(w):
                self.assertAlmostEqual(results["workers"]["wqs"].at["W" + str(wid + 1)], 1.0)
            if not config.open_ended_task:
                self.assertAlmostEqual(results["annotations"]["aqs"]["A"], 1.0)

    def test_all_workers_disagree(self):
        for w in range(2,11):
            test_config = self.test_conf_const.__class__
            data, config = crowdtruth.load(
                file = "test/" + str(w) + "work_disagr.csv",
                config = test_config())
            results = crowdtruth.run(data, config)
            self.assertAlmostEqual(results["units"]["uqs"].at[1], 0.0)
            for wid in range(w):
                self.assertAlmostEqual(results["workers"]["wqs"].at["W" + str(wid + 1)], 0.0)
                if not config.open_ended_task:
                    self.assertAlmostEqual(
                        results["annotations"]["aqs"][list(string.ascii_uppercase)[w]],
                        0.0)

    def test_outlier_worker(self):
        for w in range(3, 11):
            test_config = self.test_conf_const.__class__
            data, config = crowdtruth.load(
                file = "test/" + str(w) + "work_outlier.csv",
                config = test_config())
            results = crowdtruth.run(data, config)
            self.assertAlmostEqual(
                results["workers"]["wqs"].at["W1"],
                0.0)
            self.assertAlmostEqual(results["units"]["uqs"].at[1], 1.0)
            for x in range(1, w):
                self.assertAlmostEqual(
                    results["workers"]["wqs"].at["W" + str(x + 1)],
                    1.0)

            if not config.open_ended_task:
                self.assertAlmostEqual(
                    results["annotations"]["aqs"].at["A"],
                    0.0)
                self.assertAlmostEqual(
                    results["annotations"]["aqs"].at["B"],
                    1.0)

    
    def test_incremental_worker_agreement(self):
        for w in range(4, 11):
            test_config = self.test_conf_const.__class__
            data, config = crowdtruth.load(
                file = "test/" + str(w - 2) + "vs" + str(w - 1) + "work_agr.csv",
                config = test_config())
            results = crowdtruth.run(data, config)

            # print str(config.open_ended_task)

            # check that workers that agree on the same unit have the same quality score
            for x in range(2, w):
                if x != (w - 1):
                    self.assertAlmostEqual(
                        results["workers"]["wqs"].at["W1"],
                        results["workers"]["wqs"].at["W" + str(x)],)
                self.assertAlmostEqual(
                    results["workers"]["wqs"].at["W" + str(w)],
                    results["workers"]["wqs"].at["W" + str(w + x - 1)])

            # workers that agree have a greater WQS than the worker that disagrees
            self.assertGreater(
                results["workers"]["wqs"].at["W1"],
                results["workers"]["wqs"].at["W" + str(w - 1)])
            self.assertGreater(
                results["workers"]["wqs"].at["W" + str(w)],
                results["workers"]["wqs"].at["W" + str(2 * w - 1)])

            # the more workers agree on a unit, the higher the worker quality score
            self.assertGreater(
                results["workers"]["wqs"].at["W" + str(w)],
                results["workers"]["wqs"].at["W1"])
            # print "W" + str(w) + ": " + str(results["workers"]["wqs"].at["W" + str(w)])
            # print "W1: " + str(results["workers"]["wqs"].at["W1"])

            # the more workers agree on a unit, the higher the unit quality score
            self.assertLess(
                results["units"]["uqs"].at[1],
                results["units"]["uqs"].at[2])
            self.assertLess(
                results["units"]["uqs"].at[1],
                results["units"]["uqs"].at[3])
            self.assertLess(
                results["units"]["uqs"].at[2],
                results["units"]["uqs"].at[3])

            # the more workers agree on an annotation, the higher the unit quality score
            if not config.open_ended_task:
                self.assertLess(
                    results["annotations"]["aqs"].at["A"],
                    results["annotations"]["aqs"].at["C"])
                self.assertLess(
                    results["annotations"]["aqs"].at["B"],
                    results["annotations"]["aqs"].at["A"])
                self.assertLess(
                    results["annotations"]["aqs"].at["D"],
                    results["annotations"]["aqs"].at["C"])
                self.assertLess(
                    results["annotations"]["aqs"].at["A"],
                    results["annotations"]["aqs"].at["E"])
                self.assertLess(
                    results["annotations"]["aqs"].at["C"],
                    results["annotations"]["aqs"].at["E"])

class TestAgreementOpen(TestAgreementClosed):
    test_conf_const = TestConfigOpen()

if __name__ == '__main__':
    unittest.main()