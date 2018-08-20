#pylint: disable=E1126
""" Unit testing module for pre-processing functions """

import unittest
import string

import crowdtruth
from crowdtruth.configuration import DefaultConfig

TEST_FILE_PREF = "test/test_data/load/"

class TestConfig(DefaultConfig):
    inputColumns = ["input"]
    outputColumns = ["Answer.output"]
    open_ended_task = False
    annotation_separator = " "
    annotation_vector = list(string.ascii_uppercase)
    def processJudgments(self, judgments):
        return judgments

# test_conf_const = TestConfig()
# test_config_amt = test_conf_const.__class__
# data_amt, config_amt = crowdtruth.load(
#   file=TEST_FILE_PREF + "platform_amt" + str(1) + ".csv",
#   config=test_config_amt())

# test_config_cf = test_conf_const.__class__
# data_cf, config_cf = crowdtruth.load(
#   file=TEST_FILE_PREF + "platform_cf" + str(1) + ".csv",
#   config=test_config_cf())

class TestLoad(unittest.TestCase):
    test_conf_const = TestConfig()

    def test_platform(self):
        for w in range(1, 6):
            test_config_amt = self.test_conf_const.__class__
            data_amt, config_amt = crowdtruth.load(
                file=TEST_FILE_PREF + "platform_amt" + str(w) + ".csv",
                config=test_config_amt())
            test_config_cf = self.test_conf_const.__class__
            data_cf, config_cf = crowdtruth.load(
                file=TEST_FILE_PREF + "platform_cf" + str(w) + ".csv",
                config=test_config_cf())
            self.assertEqual(
                (set(data_cf["units"]["duration"].keys()) -
                 set(data_amt["units"]["duration"].keys())),
                set([]))
            self.assertEqual(
                (set(data_cf["workers"]["judgment"].keys()) -
                 set(data_amt["workers"]["judgment"].keys())),
                set([]))
            self.assertEqual(
                set(data_cf["workers"]["judgment"] - data_amt["workers"]["judgment"]),
                set([0]))
