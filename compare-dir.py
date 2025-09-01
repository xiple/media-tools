import argparse
import logging
import os
import hashlib
import binascii

def check_valid_directory(dir):
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Path specified for '{dir}' does not exist")

    if not os.path.isdir(dir):
        raise NotADirectoryError(f"'{dir}' is not a directory")

def checksum(filepath, hash_function="md5"):
    with open(filepath, "rb") as f:
        data = f.read()
        if hash_function == "md5":
            return hashlib.md5(data).hexdigest()
        elif hash_function == "crc32":
            return binascii.crc32(data)


def get_filepaths(path):
    all_filepaths = []
    for dirpath, _, filenames in os.walk(path):
        abspath = os.path.abspath(dirpath)
        all_filepaths += [(abspath, f) for f in filenames]
    return all_filepaths


def main(src_dir, tgt_dir):
    check_valid_directory(src_dir)
    check_valid_directory(tgt_dir) 

    src_filepaths = get_filepaths(src_dir)
    tgt_filepaths = get_filepaths(tgt_dir)
    for src_path, src_filename in src_filepaths:
        for tgt_path, tgt_filename in tgt_filepaths:
            src_filepath = os.path.join(src_path, src_filename)
            tgt_filepath = os.path.join(tgt_path, tgt_filename)

            if checksum(src_filepath, "crc32") == checksum(tgt_filepath, "crc32"):
                logger.info(f"{src_filepath} matches {tgt_filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Find files from source directory in target directory (based on file's checksum)"
        )
    )
    parser.add_argument("src_dir", type=str, help="Path to source directory")
    parser.add_argument("tgt_dir", type=str, help="Path to target directory")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s: %(message)s"
    )
    logger = logging.getLogger("compare-dir")

    main(args.src_dir, args.tgt_dir)
