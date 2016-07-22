#! python3
#########################################################################################
# IFS Importer.py                                                                       #
# Written by Kanyon Edvall                                                              #
#                                                                                       #
# This program allows the user to easily import data into IFS                           #
# More IFS functionality may be added later                                             #
#########################################################################################


#                                                                                       #
# ************************************************************************************* #
# DATA VALIDATION:                                                                      #
#   - Puts data into IFS, then goes through IFS entries (read-only) and check against   #
#     precomputed Excel values                                                          #
#   - No new data is extracted                                                          #
# ************************************************************************************* #
#                                                                                       #


#************************************ Program Setup ************************************#
# Import everything
import sys, os, re, openpyxl, getpass, base64, base64ico
import tkinter.messagebox
from tkinter import *
from tkinter import ttk, filedialog
from openpyxl.cell import get_column_letter, column_index_from_string


# Set Up GUI
root = Tk()