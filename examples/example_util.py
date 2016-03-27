from os.path import split


def get_filename(path):
    return "_".join(split(path)[-1].split(".")[:-1]) + ".gif"
