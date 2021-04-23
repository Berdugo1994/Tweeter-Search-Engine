import os
from fnmatch import fnmatch

import pandas as pd


class ReadFile:
    def __init__(self, corpus_path, iters_bulk_size=1000000):
        self.corpus_path = corpus_path
        list_of_files_to_read = self.find_data_paths_in_corpus()
        self.data_paths = [file_path for file_path in list_of_files_to_read if "ignore" not in file_path]
        self.iters_bulk_size = iters_bulk_size

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        # full_path = os.path.join(self.corpus_path, file_name)
        full_path = self.corpus_path + "/" + os.path.join(file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()

    def find_data_paths_in_corpus(self, file_type=".parquet"):
        return self.find_data_paths_in_folder(self.corpus_path, file_type)

    def find_data_paths_in_folder(self, folder_path, file_type):
        # data_paths = []
        # # for file_name in lstd(folder_path):
        # for root, subdirs, files in os.walk(folder_path):
        #     for file_name in files:
        #         if file_name.endswith(file_type):
        #             actual_file_path = root + "\\" + file_name
        #             data_paths.append(actual_file_path)
        #     for subdir in subdirs:
        #         data_paths += self.find_data_paths_in_folder(root + "\\" + subdir, file_type)
        # return data_paths
        data_paths = []
        root = folder_path
        pattern = "*" + file_type
        for path, subdirs, files in os.walk(root):
            for name in files:
                if fnmatch(name, pattern):
                    data_paths.append(os.path.join(path, name))
        return data_paths

    def __iter__(self):
        return ReadFileIterator(self.data_paths, self.iters_bulk_size)


class ReadFileIterator:
    def __init__(self, paths, bulk_size):
        self.data_paths = list(paths)
        self.bulk_size = bulk_size
        self._file_index = 0
        self._file_offset = 0
        self.current_df = None

    def __next__(self):
        if self._file_index == len(self.data_paths):
            raise StopIteration
        if self.current_df is None:
            self.current_df = pd.read_parquet(self.data_paths[self._file_index], engine="pyarrow")
        from_offset = self._file_offset
        until_offset = self._file_offset + self.bulk_size
        return_results = self.current_df[from_offset:until_offset]

        if len(self.current_df) <= until_offset:
            self._file_index += 1
            self._file_offset = 0
            self.current_df = None
        else:
            self._file_offset = until_offset

        return return_results.values.tolist()
