## **grep-sim: A grep-like command-line tool in Python**

This Python script simulates a grep-like command-line tool, allowing you to search for patterns in text files with various options and flags.

### **Features:**

- **Search:** Find lines containing a specified pattern in text files.
- **Flags:**
    - `c`: Case-sensitive search (default: case-insensitive)
    - `w`: Match whole words only
    - `n`: Count matches only
    - `i`: Invert match (find lines without the pattern)
    - `d`: Deep search (search all files within a directory and sub directory)
    - `m`: Multiple file search (search all files with wildcards within a directory)
- **Output:**
    - Highlights matched patterns in red.
    - Shows line numbers.
    - Displays the count of matches if `n` is used.

### **Usage:**

1. Run the script and you will be prompted with `:`
2. Start your command with grep then flags, pattern, location
    
    `python grep-sim.py [-c] [-w] [-n] [-i] [-d] [-m] <pattern> <path>`
    
- Replace `<pattern>` with the text you want to search for.
- Replace `<path>` with the path to a file or directory.
- Use the flags as needed:
    - `c`: For case-sensitive search.
    - `w`: To match whole words only.
    - `n`: To count matches only.
    - `i`: To find lines without the pattern.
    - `d`: To search recursively within a directory.
    - `m`: To search multiple files within a directory with wildcards (*).``

### **Example:**

 `:grep -i error log.txt`

This will search for lines that **don't** contain the word "error" in the file `log.txt`, ignoring case.

**Note:**

- The `m` flag currently doesn't support wildcards within subdirectories.
- For large files, performance might be slower due to loading the entire file into memory.

I hope this readme helps! Feel free to use and modify this script for your needs.