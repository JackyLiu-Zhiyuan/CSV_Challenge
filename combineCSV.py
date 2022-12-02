"""
file: csv_combiner.py
description: a command line program that takes several CSV files as arguments.
    Each CSV file (found in the fixtures directory of this repo) will have the same columns.
    The script outputs a new CSV file to stdout that contains the rows from each of the inputs
    along with an additional column that has the filename from which the row came (only the file's basename,
    not the entire path). The script uses 'filename' as the header for the additional column.
"""
import sys
import os
import pandas as pd


class CSVCombiner:

    def validate_file_paths(argv):
        """
        This function check if arguments entered by the users and the file-paths are valid.
        :param argv: stdin arguments
        :return: a boolean indicating if all arguments entered are valid
        """

        if len(argv) <= 1:
            print("Error: No file-paths input. Please check the format of the command line argument")
            return False

        # file_list allows multiple csv files to be combined together
        file_list = argv[1:]

        for file_path in file_list:
            if os.stat(file_path).st_size == 0:
                print("Warning: The following file is empty: " + file_path)
                return False
            if not os.path.exists(file_path):
                print("Error: File or directory not found: " + file_path)
                return False

        return True

    def combine_files(self, argv: list):
        """
        This function combines all rows in the given file list and add the filename column.
        Each row is printed to std out
        :param argv: list of valid csv file paths
        """
        buffer_size = 10 ** 6
        buffer_list = []

        if self.validate_file_paths(argv):
            file_list = argv[1:]
            for file_path in file_list:
                for chunk in pd.read_csv(file_path, chunksize=buffer_size):
                    filename = os.path.basename(file_path)
                    # append the 'filename' column
                    chunk['filename'] = filename
                    buffer_list.append(chunk)
            header = True
            # combine all columns and print to std out
            for element in buffer_list:
                print(element.to_csv(index=False, header=header, line_terminator='\n', chunksize=buffer_size), end='')
                header = False
        else:
            return

def main():
    combiner = CSVCombiner()
    combiner.combine_files(sys.argv)

if __name__ == '__main__':
    main()