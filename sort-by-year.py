import logging
import argparse
import os
import re

import piexif

img_filename_regex = re.compile(r"IMG-\d{8}-WA\d{4}\..+")
vid_filename_regex = re.compile(r"VID-\d{8}-WA\d{4}\..+")

def get_date(filename):
    return filename.split("-")[1][:7]


def get_filepaths(path, recursive):
    all_filepaths = []
    if not recursive:
        abspath = os.path.abspath(path)
        all_filepaths += [
            (abspath, f)
            for f in os.listdir(abspath)
            if os.path.isfile(os.path.join(abspath, f))
        ]
    else:
        for dirpath, _, filenames in os.walk(path):
            abspath = os.path.abspath(dirpath)
            all_filepaths += [(abspath, f) for f in filenames]
    return all_filepaths


def filter_filepaths(filepaths, allowed_ext):
    return [(fp, fn) for fp, fn in filepaths if os.path.splitext(fn)[-1] in allowed_ext]


def is_whatsapp_img(filename):
    return bool(img_filename_regex.match(filename))


def is_whatsapp_vid(filename):
    return bool(vid_filename_regex.match(filename))


def main(rootpath, recursive, month):
    if not os.path.exists(rootpath):
        raise FileNotFoundError("Path specified does not exist")

    if not os.path.isdir(rootpath):
        raise NotADirectoryError("Path specified is not a directory")

    logger.info("Listing files in target directory")
    filepaths = get_filepaths(rootpath, recursive)
    logger.info(f"Total files: {len(filepaths)}")

    allowed_extensions = set([".jpg", ".jpeg", ".mp4", ".3gp"])
    logger.info(f"Filtering for valid file extensions: {allowed_extensions}")
    filepaths = filter_filepaths(filepaths, allowed_ext=allowed_extensions)
    num_files = len(filepaths)
    logger.info(f"Valid files: {num_files}")

    logger.info("Begin processing files")
    for path, filename in filepaths:
        filepath = os.path.join(path, filename)
        targetDirectoryPath = ""

        if is_whatsapp_img(filename) or is_whatsapp_vid(filename):
            filenameYear = get_date(filename)[:4]
            filenameMonth = get_date(filename)[4:6]

            targetDirectory = os.path.join(rootpath, filenameYear)
            if month:
                targetDirectory = os.path.join(targetDirectory, filenameMonth)

            if not os.path.exists(targetDirectory):
                os.makedirs(targetDirectory, exist_ok=True)
                logger.info(f"Created {targetDirectory}")

            targetDirectoryPath = os.path.join(targetDirectory, filename)
            os.rename(filepath, targetDirectoryPath)

            logger.info(f"Moved {filepath} to {targetDirectoryPath}")
        else:
            try:
                exif_dict = piexif.load(filepath)
                dateTimeOriginal = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
                if dateTimeOriginal:
                    yearOriginal = dateTimeOriginal.decode("utf-8")[:4]
                    targetDirectory = os.path.join(rootpath, yearOriginal)

                    if month:
                        monthOriginal = dateTimeOriginal.decode("utf-8")[5:7]
                        targetDirectory = os.path.join(targetDirectory, monthOriginal)

                    if not os.path.exists(targetDirectory):
                        os.makedirs(targetDirectory, exist_ok=True)
                        logger.info(f"Created {targetDirectory}")
                else:
                    targetDirectory = os.path.join(rootpath, "Unknown")
                    if not os.path.exists(targetDirectory):
                        os.mkdir(targetDirectory)
                        logger.info(f"Created {targetDirectory}")

                targetDirectoryPath = os.path.join(targetDirectory, filename)
                os.rename(filepath, targetDirectoryPath)

                logger.info(f"Moved {filepath} to {targetDirectoryPath}")
            except piexif.InvalidImageDataError:
                logger.warning(f"{filename} : invalid image data, skipping")
                continue

    logger.info("Finished processing files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("TODOTODO"))
    parser.add_argument("rootpath", type=str, help="Path to pictures folder")
    parser.add_argument(
        "-r",
        "--recursive",
        default=False,
        action="store_true",
        help="Recursively process media",
    )
    parser.add_argument(
        "-m",
        "--month",
        default=False,
        action="store_true",
        help="Create month directories along with year directories",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s: %(message)s"
    )
    logger = logging.getLogger("sort-by-year")

    main(args.rootpath, args.recursive, args.month)
