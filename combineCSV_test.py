"""
file: test_csv_combiner.py
description: a set of unit tests used to test ./csv_combiner.py
author: abdullah al hamoud
"""

import sys
from csv_combiner import CSVCombiner
import os
import pandas as pd
import unittest
from io import StringIO
import test_generatefixtures


class TestCombineMethod(unittest.TestCase):

    # initialize all paths
    test_output_path = "./test_output.csv"
    csv_c_path = "./csv_combiner.py"
    acc_path = "./test_fixtures/accessories.csv"
    clo_path = "./test_fixtures/clothing.csv"
    hc_path = "./test_fixtures/household_cleaners.csv"
    ef_path = "./test_fixtures/empty_file.csv"

    backup = sys.stdout
    test_output = open(test_output_path, 'w+')
    combiner = CSVCombiner()

    """
    This function generates the test fixture files located in ./test_fixtures/ 
    and redirect the output to ./test_output.csv
    """
    def setUpClass(cls):
        test_generatefixtures.main()
        sys.stdout = cls.test_output

    def tearDownClass(cls):

        cls.test_output.close()
        if os.path.exists(cls.hc_path):
            os.remove(cls.hc_path)
        if os.path.exists(cls.clo_path):
            os.remove(cls.clo_path)
        if os.path.exists(cls.acc_path):
            os.remove(cls.acc_path)
        if os.path.exists(cls.test_output_path):
            os.remove(cls.test_output_path)
        if os.path.exists(cls.ef_path):
            os.remove(cls.ef_path)
        if os.path.exists("./test_fixtures"):
            os.rmdir("./test_fixtures")

    def tearDown(self):
        self.test_output.close()
        self.test_output = open(self.test_output_path, 'w+')
        sys.stdout = self.backup
        self.test_output.truncate(0)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

    def setUp(self):
        # setup
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.test_output_path, 'w+')

    """
    This function test if the error message is correctly sent out when there is no file path
    """
    def test_no_file_paths(self):
        argv = [self.csv_c_path]
        self.combiner.combine_files(argv)

        self.assertIn("Error: No file-paths input.", self.output.getvalue())

    """
    This function test if the error message is correctly sent out when input file is empty
    """
    def empty_files_test(self):
        argv = [self.csv_c_path, self.ef_path]
        self.combiner.combine_files(argv)
        self.assertIn("Warning: The following file is empty: ", self.output.getvalue())

    """
    This function test if the error message is correctly sent out when input file does not exist
    """
    def non_existent_files_test(self):
        argv = [self.csv_c_path, "non_existent.csv"]
        self.combiner.combine_files(argv)
        self.assertTrue("Error: File or directory not found:" in self.output.getvalue())

    """
     This function test the normal user case when all values exist in the combined file
     """

    def all_values_exist_in_combined_happy_trail(self):
        argv = [self.csv_c_path, self.acc_path, self.clo_path,
                self.hc_path]
        self.combiner.combine_files(argv)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()
        acc = pd.read_csv(filepath_or_buffer=self.acc_path, lineterminator='\n')
        clo = pd.read_csv(filepath_or_buffer=self.clo_path, lineterminator='\n')
        hc = pd.read_csv(filepath_or_buffer=self.hc_path, lineterminator='\n')
        with open(self.test_output_path) as f:
            combined_df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertEqual(len(combined_df.merge(clo)), len(combined_df.drop_duplicates()))
        self.assertEqual(len(combined_df.merge(hc)), len(combined_df.drop_duplicates()))
        self.assertEqual(len(combined_df.merge(acc)), len(combined_df.drop_duplicates()))

    """
    This function test the normal user case when filename is added to roles
    """
    def filename_added_to_rows_happy_trail(self):
        argv = [self.csv_c_path, self.acc_path, self.clo_path]
        self.combiner.combine_files(argv)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()
        with open(self.test_output_path) as f:
            df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertIn('accessories.csv', df['filename'].tolist())

    """
    This function test the normal user case when filename column is added
    """
    def filename_column_added_happy_trail(self):

        argv = [self.csv_c_path, self.acc_path, self.clo_path]
        self.combiner.combine_files(argv)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()
        with open(self.test_output_path) as f:
            df = pd.read_csv(f)
        self.assertIn('filename', df.columns.values)



