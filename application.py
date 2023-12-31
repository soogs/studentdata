# app.py #
# module for creating the Flask App

import pickle
import dill
from flask import Flask, request, render_template, jsonify

import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, StandardScaler

# importing the CustomData class that takes the input in and makes it into df
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

## Route for a home page

@app.route('/')
def index():

	# data_prior = CustomData(gender = "male", 
	# 	race_ethnicity = "group B",
	# 	parental_level_of_education = "some college",
	# 	lunch = "standard",
	# 	test_preparation_course = "none",
	# 	reading_score = 22,
	# 	writing_score = 33)

	# pred_df_prior = data_prior.get_data_as_data_frame()

	# return render_template("index.html", gender_prior = "male", prior_prediction = pred_df_prior.iloc[0,0])
	return render_template("index.html")

# specifying two methods of GET and POST
@app.route('/predictdata', methods = ['GET', 'POST'])
def predict_datapoint():
	# getting the data, and doing the prediction here
	if request.method == 'GET':
		return render_template('home.html')
		# for the method GET, we just have the input field for the users

	else:
		# let's create the data for the POST method

		# 'request' collects the input data on the web app
		data = CustomData(
			gender = request.form.get('gender'),
			race_ethnicity = request.form.get('race_ethnicity')	,
			parental_level_of_education = request.form.get('parental_level_of_education'),
			lunch = request.form.get('lunch'),
			test_preparation_course = request.form.get('test_preparation_course'),
			reading_score = float(request.form.get('reading_score')),
			writing_score = float(request.form.get('writing_score'))
		)

		# this 'get_data_as_data_frame' function is within the CustomData class
		pred_df = data.get_data_as_data_frame()

		# initialize the pipeline for prediction
		predict_pipeline = PredictPipeline()
		results = predict_pipeline.predict(pred_df)

		return render_template('home.html', results = round(results[0],3))

if __name__ == "__main__":
	app.debug = True
	app.run()


		

