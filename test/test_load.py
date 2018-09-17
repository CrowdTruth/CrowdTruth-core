""" Unit testing module for pre-processing functions """

import unittest
import string
import pandas as pd

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

class ConfigKeepEmptyRows(TestConfig):
    remove_empty_rows = False

class ConfigProcessJudg(TestConfig):
    def processJudgments(self, judgments):
        for col in self.outputColumns:
            judgments[col] = judgments[col].apply(lambda x: str(x).lower())
        return judgments

class TestLoad(unittest.TestCase):
    test_conf_const = TestConfig()
    test_keep_empty_rows = ConfigKeepEmptyRows()
    test_process_judg = ConfigProcessJudg()

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

    def test_empty_rows(self):
        test_without = self.test_conf_const.__class__
        data_without, _ = crowdtruth.load(
            file=TEST_FILE_PREF + "empty_rows.csv",
            config=test_without())
        self.assertEqual(data_without["judgments"].shape[0], 24)

        test_proc_judg = self.test_process_judg.__class__
        data_proc_judg, _ = crowdtruth.load(
            file=TEST_FILE_PREF + "empty_rows.csv",
            config=test_proc_judg())
        self.assertEqual(data_proc_judg["judgments"].shape[0], 24)

        test_with = self.test_keep_empty_rows.__class__
        data_with, _ = crowdtruth.load(
            file=TEST_FILE_PREF + "empty_rows.csv",
            config=test_with())
        self.assertEqual(data_with["judgments"].shape[0], 27)

    def test_data_frame(self):
        for w in range(1, 6):
            test_config_file = self.test_conf_const.__class__
            data_file, _ = crowdtruth.load(
                file=TEST_FILE_PREF + "platform_cf" + str(w) + ".csv",
                config=test_config_file())
            df = pd.read_csv(TEST_FILE_PREF + "platform_cf" + str(w) + ".csv")
            test_config_df = self.test_conf_const.__class__
            data_df, _ = crowdtruth.load(
                data_frame=df,
                config=test_config_df())
            self.assertEqual(
                (set(data_df["units"]["duration"].keys()) -
                 set(data_file["units"]["duration"].keys())),
                set([]))
            self.assertEqual(
                (set(data_df["workers"]["judgment"].keys()) -
                 set(data_file["workers"]["judgment"].keys())),
                set([]))
            self.assertEqual(
                set(data_df["workers"]["judgment"] - data_file["workers"]["judgment"]),
                set([0]))




