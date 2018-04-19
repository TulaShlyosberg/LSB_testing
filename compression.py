from zipfile import ZipFile


def compress(filepath, zippath):
    archive = ZipFile(zippath, 'w')
    archive.write(filepath)
    archive.close()
