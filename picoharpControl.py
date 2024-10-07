# Based on a Demo for access to PicoHarp 300 Hardware via PHLIB.DLL v 3.0. by Keno Goertz, PicoQuant GmbH, February 2018
# This version was compiled/modified by Matthew Larson on october 7th 2024 
# This is a back end which handles picoharp connections

import time
import ctypes as ct
from ctypes import byref


# From phdefin.h
LIB_VERSION = "3.0"
HISTCHAN = 65536
MAXDEVNUM = 8
MODE_HIST = 0
FLAG_OVERFLOW = 0x0040

# Measurement parameters, these are hardcoded since this is just a demo
binning = 0 # you can change this
offset = 0
tacq = 1000 # Measurement time in millisec, you can change this
syncDivider = 1 # you can change this 
CFDZeroCross0 = 10 # you can change this (in mV)
CFDLevel0 = 100 # you can change this (in mV)
CFDZeroCross1 = 10 # you can change this (in mV)
CFDLevel1 = 50 # you can change this (in mV)
cmd = 0

# Variables to store information read from DLLs
counts = (ct.c_uint * HISTCHAN)()
dev = []
libVersion = ct.create_string_buffer(b"", 8)
hwSerial = ct.create_string_buffer(b"", 8)
hwPartno = ct.create_string_buffer(b"", 8)
hwVersion = ct.create_string_buffer(b"", 8)
hwModel = ct.create_string_buffer(b"", 16)
errorString = ct.create_string_buffer(b"", 40)
resolution = ct.c_double()
countRate0 = ct.c_int()
countRate1 = ct.c_int()
flags = ct.c_int()