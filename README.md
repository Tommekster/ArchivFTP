# Archiv FTP

`ArchivFTP` is python based FTP server. Main facility is to store all files gzipped on FTP server.

```
./some_folder/some_file.txt => ArchivFTP => /var/ftp_storage/some_folder/some_file.txt.gz
./some_folder/some_file.txt <= ArchivFTP <= /var/ftp_storage/some_folder/some_file.txt.gz
```

Let's say that you have some files that you don't want to delete but you don't use them often.
Now you can move them to archive using FTP client.
Files are stored at the ArchivFTP server and automatically compressed.
Compression saves your ArchivFTP storage space.

Whenever you want to get your archived files, connect the ArchivFTP server.
Download the files. They are automaticaly uncompressed.

## Instalation

```
git clone https://github.com/Tommekster/ArchivFTP.git
cd ArchivFTP

virualenv -p python3 venv
. ./venv/bin/activate
# venv\Scripts\activate.bat # on windows

pip install -r requirements.txt

python main.py
```

You can edit parameters at the beggining of the `main.py` file.

## Usage

1. Open `ftp://my_user:change_this_password@localhost:2121/`.
2. Copy your files
