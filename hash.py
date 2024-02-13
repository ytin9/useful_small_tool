import subprocess
import sys

def check_and_install_packages(packages):
    for package in packages:
        try:
            __import__(package)
            print(f"Package '{package}' is already installed.")
        except ImportError:
            print(f"Package '{package}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["send2trash", "tqdm"]

# Check and install if necessary
check_and_install_packages(required_packages)

# The rest of your script starts here...
import os
import hashlib
from collections import defaultdict
import send2trash
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # 导入tqdm库

def calculate_md5(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_hash(file_path):
    """返回文件路径和其MD5哈希值"""
    return file_path, calculate_md5(file_path)

def find_duplicate_files(directory):
    """查找目录中的重复文件"""
    hashes = defaultdict(list)
    files_to_check = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_to_check.append(os.path.join(root, file))

    # 使用tqdm显示进度条
    with ThreadPoolExecutor(max_workers=4) as executor, tqdm(total=len(files_to_check), desc="Scanning files") as progress:
        future_to_hash = {executor.submit(file_hash, file_path): file_path for file_path in files_to_check}
        for future in as_completed(future_to_hash):
            progress.update(1)  # 每完成一个任务就更新进度条
            try:
                file_path, file_hash_result = future.result()
                hashes[file_hash_result].append(file_path)
            except Exception as exc:
                print(f'{file_path} generated an exception: {exc}')

    return {hash_value: paths for hash_value, paths in hashes.items() if len(paths) > 1}

def main(directory):
    """主函数"""
    duplicates = find_duplicate_files(directory)
    to_be_moved = []

    if duplicates:
        print("\nDuplicate files found:")
        for hash_value, files in duplicates.items():
            print(f"Hash: {hash_value}")
            for file in files[1:]:  # Skip the first file
                print(f"- {file}")
                to_be_moved.append(file)

        if to_be_moved:
            print("\nThe following files will be moved to the trash:")
            for file in to_be_moved:
                print(file)
            print("\nDo you want to proceed? (YES/no)")
            response = input().strip().lower()
            if response == "" or response == "yes" or response == "y":
                for file in to_be_moved:
                    send2trash.send2trash(file)
                    print(f"Moved to trash {file}")
            else:
                print("Operation cancelled.")
    else:
        print("No duplicate files found.")

    print("\nFinal files in the directory:")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

if __name__ == "__main__":
    directory = input("Enter the directory path to check for duplicate video files: ")
    main(directory)
