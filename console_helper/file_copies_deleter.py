import os
from os import walk
import hashlib
import time
from os.path import join, getsize

from .colors import G, R, N, Y

# Getting an absolut path to directory with files
# def get_path_dir():
#     abs_path = input("Please, enter the absolute path to directory: ")
#     if len(abs_path) == 0:
#         print("Directory is not specified. Try again.\n")
#     elif os.path.isdir(abs_path):
#         return abs_path
#     else:
#         print("Entered path doesn't exist. Try again.\n")


def count_files(abs_path, file_format=""):
    total_count_files = 0

    for root, _, files in walk(abs_path, topdown=True):
        for file in files:
            if file.endswith(file_format):
                total_count_files += 1

    print(f"{G}Files found:{N} {Y}{total_count_files}{N}")


# The function takes absolute path to file and returns its hash
def get_hash(path_to_file):
    blocksize = 65536
    file_hash = hashlib.md5(open(path_to_file, "rb").read(blocksize)).hexdigest()
    return file_hash


# This function returns the number of copies found and the dictionary as
# {hash_1: [path_to_file1, path_to_file1...], hash_2: [path_to_file3, path_to_file4...]...}
def count_copies(dir_path, file_format=""):
    copy_count = 0
    hash_dict = {}

    for root, _, files in walk(dir_path, topdown=True):
        for file in files:
            if file.endswith(file_format):
                file_path = join(root, file)  # Absolut path to file

                file_hash = get_hash(file_path)  # File's hash

                if file_hash in hash_dict.keys():
                    copy_count += 1
                    hash_dict[file_hash].append(file_path)
                else:
                    hash_dict[file_hash] = [file_path]

    return copy_count, hash_dict


# Check if the hash key is already in the dictionary; if it is, delete the new file by its path
def delete_files(hash_dictionary):
    total_deleted = 0
    for path_dict in hash_dictionary.values():
        for file_path in path_dict[1:]:
            total_deleted += getsize(file_path) / (1024 * 1024)  # size in MB
            os.remove(file_path)  # Deleting a file

    return round(total_deleted, 2)


# The function deletes empty folders that may have formed after deleting copies
def delete_empty_folders(path):
    for element in os.scandir(path):
        if os.path.isdir(element):
            full_path = os.path.join(path, element)
            delete_empty_folders(full_path)  # recursion
            if not os.listdir(full_path):
                os.rmdir(full_path)  # remove empty folder


def copies_deleter(root):
    path_to_dir = root
    count_files(path_to_dir)

    print("Looking for copies...")
    time.sleep(0.5)

    copy_count, hash_dict = count_copies(path_to_dir)
    print(f"{G}Copies found:{Y} {copy_count}{N}")

    if copy_count != 0:
        while True:
            want_delete = input(
                f"{G}Do you want to delete the detected copies (y/n)?{N} "
            )

            if want_delete in ("yes", "YES", "Y", "y"):
                total_deleted = delete_files(hash_dict)
                print(f"Deleted {total_deleted} МВ")
                time.sleep(3)
                break
            elif want_delete in ("n", "N", "no", "NO"):
                print(f"{G}Ok{N}")
                time.sleep(2)
                break
            else:
                print(f"{R}You entered a non-existent command. Please try again.{N}\n")

        delete_empty_folders(path_to_dir)
    return "Done"


if __name__ == "__main__":
    copies_deleter("d:\\Different\\Garbage\\")
