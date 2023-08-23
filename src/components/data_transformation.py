# data transformation #
# in this module, we do the pre-processing of the data

import sys
from dataclasses import dataclass
import os

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# exception handling
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


# what is the use of the dataclass here?
@dataclass
class DataTransformationConfig:
# this provides any path, input that are needed for the
# data transformation

	# providing the pickle file
	preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")
	# os.path.join just combines the "artifacts" and "preprocessor.pkl"
	# in a path format. It does not concern with parent directories


class DataTransformation:
	def __init__(self):
		self.data_transformation_config = DataTransformationConfig()
		# initialzing "data_transformation_config"
		# as the path provied by above Class

	def get_data_transformer_object(self):
		'''
		Function that provides the pipelines for 
		data transformation (pre-processing)
		'''

		# create all the pickle files, for
		# performing data processing and standardizing

		try:
			# numeric_features = [feature for feature in df.columns if df[feature].dtype != 'O']
			# categorical_features = [feature for feature in df.columns if df[feature].dtype == 'O']
			# this extracts the feature names of the numeric and categorical features
			# the above code did not work because we did not yet read the data

			# numerical_features = ['math_score', 'reading_score', 'writing_score']
			numerical_features = ['reading_score', 'writing_score']
			categorical_features = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

			# logging the found features
			logging.info(f"Numerical features are: {numerical_features}")
			logging.info(f"Categorical features are: {categorical_features}")

			# let's create a pipeline for numerical features
			num_pipeline = Pipeline(

				steps = [
					("imputer", SimpleImputer(strategy = "median")),
					("scaler", StandardScaler())
				]
			)

			logging.info("Numerical features processed")

			cat_pipeline = Pipeline(

				# imputing the missing value with most frequent level

				steps = [
					("imputer", SimpleImputer(strategy = "most_frequent")),
					("one_hot_encoder", OneHotEncoder())
					# ("scaler", StandardScaler())

				]

			)

			logging.info("Categorical features processed")

			# combining the Pipeline for the numerical and categorical features
			# for that, we need the ColumnTransformer
			preprocessor = ColumnTransformer(
				[
				("num_pipeline", num_pipeline, numerical_features),
				("cat_pipeline", cat_pipeline, categorical_features)
				]

			)

			# returning the final pipeline
			return preprocessor

		except Exception as e:
			raise CustomException(e, sys)

	def initiate_data_transformation(self, train_path, test_path):

		try:
			train_df = pd.read_csv(train_path)
			test_df = pd.read_csv(test_path)

			# print("train_df, after ingestion and splitting \n", train_df.head)
			# print("test_df, after ingestion and splitting \n", test_df.head)

			logging.info("Train and test data imported.")

			logging.info("Obtaining the pre-processing object")

			preprocessing_obj = self.get_data_transformer_object()
			# this pre-processing pipeline (object)
			# should later be converted into a pickle file
			# and be saved

			logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
			
			target_column_name = "math_score"

			input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)

			target_feature_train_df=train_df[target_column_name]

			input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)

			target_feature_test_df=test_df[target_column_name]

			logging.info(
				f"Applying preprocessing object on training dataframe and testing dataframe."
			)

			# so the pipeline is only placed upon the input features!
			input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
			input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

			train_arr = np.c_[
				input_feature_train_arr, np.array(target_feature_train_df)
			]

			test_arr = np.c_[
				input_feature_test_arr, np.array(target_feature_test_df)
			]


			# print("train_arr, from transformation \n", train_arr[:2,])
			# print("test_arr, from transformation \n", test_arr[:2,])

			logging.info(f"Saved preprocessing object.")

			# utils.py..
			# saving the pre-processing pipeline
			save_object(
				file_path = self.data_transformation_config.preprocessor_obj_file_path,
				obj = preprocessing_obj
			)

			return (
			    train_arr,
			    test_arr,
			    self.data_transformation_config.preprocessor_obj_file_path,
			)

		except Exception as e:
			raise CustomException(e, sys)