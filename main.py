import hashlib
import os
import sys


class HashFile:
    file_name = None
    hash_alg = None
    result = None

    def __init__(self, file_name, hash_alg, result):
        self.file_name = file_name
        self.hash_alg = hash_alg
        self.result = result


class HashFileParser:
    @staticmethod
    def get_hash_alg(title):
        if title == 'md5':
            return hashlib.md5
        elif title == 'sha1':
            return hashlib.sha1
        elif title == 'sha256':
            return hashlib.sha256

    @staticmethod
    def get_files(file_name='hash_files.bin', files_path='files'):
        files = []
        try:
            with open(file_name, 'r') as f:
                for line in f.read().split('\n'):
                    if line.strip() == '':
                        continue
                    file = line.split()
                    files.append(HashFile(file_name=files_path + '\\' + file[0],
                                          hash_alg=HashFileParser.get_hash_alg(file[1]),
                                          result=file[2]
                                          ))
            return files

        except FileNotFoundError:
            print('File not found: ' + os.getcwd() + '\\' + file_name)
        except IndexError:
            print('Error during analyzing checking file')

        return None


class FilesChecker:
    FLAGS = {
        'OK': 'OK',
        'FAIL': 'FAIL',
        'NF': "NOT FOUND",
        'FE': 'FATAL ERROR',
    }

    def compare_files(self, files):
        results = {}
        for file in files:
            results[file.file_name] = self.FLAGS[self.compare_file(file)]
        return results

    def compare_file(self, file):
        try:
            with open(file.file_name, 'r') as f:
                if file.hash_alg(f.read().encode()).hexdigest() == file.result:
                    return 'OK'
            return 'FAIL'
        except FileNotFoundError:
            return 'NF'

        return 'FE'


if __name__ == '__main__':
    if len(sys.argv) > 2:
        files = HashFileParser.get_files(sys.argv[1], sys.argv[2])
    else:
        files = HashFileParser.get_files()
        hash_files_path = ''

    if files:
        checker = FilesChecker()
        results = checker.compare_files(files)
        for file in results:
            print(file + ' ' + results[file])
