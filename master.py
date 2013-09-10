"""
Add the path to Python, then imports and reloads run.
There is no need to change this file.

Copyright Robbert Bloem, 2013
"""

import sys
import os
import bpy

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

import imp
import run
imp.reload(run)