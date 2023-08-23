# utils.py # 
# this file provides the common functionalities used in the project

import os
import sys

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
import dill

# creating a function for saving objects that can be used 
# globally in the project. It saves as a pickle file,
# using dill.


def save_object (file_path, obj):
	try:
		dir_path = os.path.dirname(file_path)

		os.makedirs(dir_path, exist_ok = True)

		with open (file_path, "wb") as file_obj:
			dill.dump(obj, file_obj)

	except Exception as e:
		raise CustomException(e, sys)