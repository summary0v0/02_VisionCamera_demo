def ini_file(path):
    with open(path) as f:
        lines = f.readlines()
        f.close()
        return lines
