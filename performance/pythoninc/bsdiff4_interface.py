# bsdiff4_interface.py

import bsdiff4

def create_patch(oldfile, newfile, patchfile):
    bsdiff4.file_diff(oldfile, newfile, patchfile)
    return "Patch file created successfully."

def apply_patch(oldfile, patchfile, newfile):
    bsdiff4.file_patch(oldfile, patchfile, newfile)
    return "Patch applied successfully."
