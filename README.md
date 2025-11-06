# whatsapp-media-tools

Python scripts to manage WhatsApp media backups for archival purposes.

## Prerequisites

Scripts are using python `piexif` module to manage exif metadata.

Best practice is to create a virtual environment to manage dependencies. Below commands example for bash shell :

```bash
# Create a virtual environment named 'myenv'
python3 -m venv myvenv

# Source virtual env variables
source myvenv/bin/activate

# Check paths
which python3
which pip3

# Install python module requirements in the virtual env
python3 -m pip install -r requirements.txt

# once finished with scripts, deactivate the virtual env
deactivate
```

## Usage

### Restoring exif dates

```text
usage: restore-exif.py [-h] [-r] [-m] path

Restore discarded Exif date information in WhatsApp media based on the filename. For videos, only the created and modified dates are set.

positional arguments:
  path             Path to WhatsApp media folder

options:
  -h, --help       show this help message and exit
  -r, --recursive  Recursively process media
  -m, --mod        Set file created/modified date on top of exif for images
```

### Finding duplicate media files

```text
usage: find-duplicates.py [-h] [-c CHUNK_SIZE] [-f] [-r] [--dry-run] path

Remove duplicated media, preserving the file with the shortest filename or earliest date encoded in the filename.

positional arguments:
  path                  Path to WhatsApp media folder

options:
  -h, --help            show this help message and exit
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        Chunk size for heuristic, smaller values are generally faster but if many files have identical starting chunks, performance degrades as more full hashes are computed
  -f, --force           Delete duplicates without prompting
  -r, --recursive       Recursively process media
  --dry-run             Dry run deletion (no files deleted)
  ```

### Stow pictures by year/month

```text
usage: sort-by-year.py [-h] [-r] [-m] rootpath

Stow pictures in directories 'year' based on picture exif metadata or whatsapp filename date

positional arguments:
  rootpath         Path to pictures folder

options:
  -h, --help       show this help message and exit
  -r, --recursive  Recursively process media
  -m, --month      Create month directories along with year directories
```
