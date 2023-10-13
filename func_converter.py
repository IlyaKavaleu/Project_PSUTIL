def count_MB(count_bytes, suffix='B'):
    """A counting function that converts bytes into GB, if necessary"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if count_bytes < factor:
            return f"{count_bytes:.2f}{unit}{suffix}"
        count_bytes /= factor
