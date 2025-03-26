def sanitize_filename(filename):
    return filename.replace(" ", "-").replace("_", "-")

def format_path(path):
    return path.replace("\\", "/")
