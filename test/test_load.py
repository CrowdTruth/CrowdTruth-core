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

class TestLoad(unittest.TestCase):
    test_conf_const = TestConfig()

    def test_platform(self):
        for w in range(1, 6):
            test_config_amt = self.test_conf_const.__class__
            data_amt, _ = crowdtruth.load(
                file=TEST_FILE_PREF + "platform_amt" + str(w) + ".csv",
                config=test_config_amt())
            test_config_cf = self.test_conf_const.__class__
            data_cf, _ = crowdtruth.load(
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

    def test_folder(self):
        test_config = self.test_conf_const.__class__
        data, _ = crowdtruth.load(
            directory=TEST_FILE_PREF + "dir/",
            config=test_config())
        self.assertEqual(data["workers"].shape[0], 7)
        self.assertEqual(data["units"].shape[0], 2)
        self.assertEqual(data["judgments"].shape[0], 12)
