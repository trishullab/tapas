def foo(x : int, y : str): ...

xy = {'x' : 1, 'y' : 'hello'} 

foo(**xy)

# import ntpath
# import os
# import sys
# import tkFileDialog
# import tkMessageBox
# import traceback
# import ttk

# try:
#     from Tkinter import *
# except ImportError:
#     print("Tkinter library is not available.")
#     exit(0)

# path = os.path.dirname(sys.modules[__name__].__file__)
# path = os.path.join(path, '..')
# sys.path.insert(0, path)
# from spatialmedia import metadata_utils

# SPATIAL_AUDIO_LABEL = "My video has spatial audio (ambiX ACN/SN3D format)"
# HEAD_LOCKED_STEREO_LABEL = "with head-locked stereo"

# class Console(object):
#     def __init__(self):
#         self.log = []

#     def append(self, text):
#         print(text.encode('utf-8'))
#         self.log.append(text)


# class Application(Frame):
#     def action_open(self):
#         """Triggers open file diaglog, reading a new file's metadata."""
#         tmp_in_file = tkFileDialog.askopenfilename(**self.open_options)
