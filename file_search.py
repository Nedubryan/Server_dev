import mmap
import re
import subprocess
import os

REREAD_ON_QUERY = False


def load_file(filepath):
    """Reads the entire file into a list of lines."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()

def search_in_list(lines, query):
    """Search for exact match in list of lines (used when rereading is disabled)."""
    query = query.strip()
    return any(line.strip() == query for line in lines)

def search_in_lines(lines, query):
    """Search for exact match in provided list of lines."""
    query = query.strip()
    return any(line.strip() == query for line in lines)

def search_with_mmap(file_path, query):
    """Platform-safe search using mmap."""
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return False

        query_bytes = query.encode("utf-8")
        with open(file_path, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                return mm.find(query_bytes) != -1
    except Exception as e:
        from server.logger import setup_logger
        logger = setup_logger()
        logger.error(f"[mmap search error] {e}")
        return False

def search_with_regex(filepath, query):
    """Search using regex pattern match."""
    pattern = re.compile(rf"^{re.escape(query)}$", re.MULTILINE)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return bool(pattern.search(f.read()))

def search_with_grep(file_path, search_term):
    """
    Portable version: scans a file line by line and checks if the term exists.
    Compatible with both Windows and Unix environments.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if search_term in line:
                    return True
        return False
    except Exception:
        return False

