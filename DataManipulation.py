#####################################################################################
# DataManipulation Class Object used to query csv files and shp files
# 	Funcions include:
#		- addCSV() - adds a single CSV to a list from a single file
# 		- addCSVs() - adds a group of CSVs to a list from a directory
#		- addExcel() - adds a single Excel sheet or multiple Excel sheets
#		- addShape() - adds a SHP to a list from a single file
#####################################################################################
import csv
import os
import glob
import geopandas as gpd
import pandas as pd
import numpy as np
import scipy.stats
from mpmath import *
from shapely.geometry import Point

class DataManipulation(object):

# INSTANCE VARIABLES:
	
	# Variables are accessible within this class using _ and __ 
	csv = list
	shape = list
	df = pd.DataFrame()
	gdf = gpd.GeoDataFrame()

# CONSTRUCTOR METHODS:

	# Constructor method which creates instance variables
	# Instance variables consiste of lists plus one output file
	# The methodology is that like files are stored in lists and later merged
	def __init__(self):
		self.csv = []
		self.shape =[]
		self.df = pd.DataFrame()
		self.gdf = gpd.GeoDataFrame()

# SETTER METHODS:

	# addCSV() - appends a single dataframe to the instance variable 'csv' from a CSV file 
	# parameters include directory of CSV and file name of CSV to append
	def addCSV(self, directory, file):
		os.chdir(directory)
		csv = open(file)	
		df = pd.read_csv(file, sep=',')
		df.columns = df.columns.str.strip()
		df.columns = map(str.upper, df.columns)
		df = df.dropna(axis=1, how='all')	
		self.csv.append(df)


	# addURL() - appends a single dataframe to the instace variable 'csv' from a url
	# parameters include the url link
	def addURL(self, url):
		df = pd.read_csv(url, dtype={'GEOID':'str'}, sep='\t')
		df.columns = df.columns.str.strip()
		df.columns = map(str.upper, df.columns)
		df = df.dropna(axis=1, how='all')
		self.csv.append(df)


	# addCSVs() - appends a dataframe csv from a series of CSV files within a directory
	# parameters include the directory of the series of CSV files to convert to a dataframe
	def addCSVs(self, directory):
		os.chdir(directory)
		all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
		df = pd.concat([pd.read_csv(f) for f in all_filenames])
		df.columns = df.columns.str.strip()
		df.columns = map(str.upper, df.columns)
		df = df.dropna(axis=1, how='all')
		self.csv.append(df)

	# addExcel() - appends an xlsx or xls file and/or its sheets to variable 'csv'
	# parameters include the directory of the file, file name, and name of sheets
	def addExcel(self, directory, file, sheet):
		os.chdir(directory)	
		df = pd.read_excel(file, sheet_name=sheet, header=0, comment='#')
		df.columns = df.columns.str.strip()
		df.columns = map(str.upper, df.columns)
		df = df.dropna(axis=1, how='all')
		self.csv.append(df)


	# addShape() - appends a shape file to self.shape list
	# parameters include the directory of the shapefile and the file name of the shapefile		
	def addShape(self, directory, file):
		os.chdir(directory)
		self.shape.append(gpd.read_file(file))


# SETTER METHODS:

	# setData() - sets all columns to string objects
	#
	def setDataTypeString(self):
		for i in range(len(self.csv)):
			for col in self.csv[i].columns:
				self.csv[i][col] = self.csv[i][col].apply(str)

	# setDataFloat() - sets all columns to floats
	#
	def setDataFloat(self):
		for i in range(len(self.csv)):
			for col in self.csv[i].columns:
				self.csv[i][col] = self.csv[i][col].astype(float)

	# # setDataTypeFloat() - prompts user for columns to set to floats
	# #
	# def setDataTypeFloat(self):
	# 	for i in range(len(self.csv)):
	# 		print(self.csv[i].info())
	# 		col = input('Which column to convert to float?    ')
	# 		self.csv[i][col] = self.csv[i][col].astype(float)
	
	# setKey() - prompts user to set a column to a string object as a key value
	#
	def setKey(self):
		for i in range(len(self.csv)):

			isKey = input("Is there a column key? (y or n)    ")
			if isKey == 'y':
				print(self.csv[i].info())
				key = input("Which column header is the key value?    ")
				self.csv[i][key] = self.csv[i][key].apply(str)
			
			for col in self.csv[i].columns:
				if col != key:
					self.csv[i][col] = self.csv[i][col].apply(str)


	# removeLastColumn() - method automatically removes the last column of the dataframe
	#
	def removeLastColumn(self):
		for i in range(len(self.csv)):

			self.csv[i].drop(self.csv[i].columns[len(self.csv[i].columns)], axis='columns', inplace=True)


	# removeColumnHeaders() - prompts the client if they would like to remove any column headers and makes the requested
	# change per the client's input
	def removeColumnFromTable(self):

		# Identify if columns are to be removed from dataframe in self.csv
		isKey = input("Remove columns from dataframe? (y or n)    ")
		if isKey == 'y':

			rem = input("Remove by column name or column index? (name or index)    ")
			
			if rem == 'name':
				var = []
				keyboard = 'begin'

				for i in range(len(self.csv)):
					print(self.csv[i].info())

					while keyboard != 'done':
						print(self.csv[i].info())
						keyboard = input("Which column names to remove from the dataframe? (Type 'done' to exit)    ")
						if keyboard != 'done':
							self.csv[i] = self.csv[i].drop(columns=[keyboard.upper()])


			if rem == 'index':
				index = -1
				keyboard = 'begin'

				for i in range(len(self.csv)):

					while keyboard != 'done':
						print(self.csv[i].info())
						keyboard = input("Which column indexes to remove from the dataframe? (Type 'done' to exit)    ")
						if keyboard != 'done':
							self.csv[i].drop(self.csv[i].columns[int(keyboard)], axis='columns', inplace=True)


	# removeColumnFromShapefile() - prompts the client if they would like to remove any column headers and makes the requested
	# change per the client's input
	def removeColumnFromShapefile(self):
		# Identify if columns are to be removed from shapefile in self.shape
		isKey = input("Remove columns for shapefile? (y or n)    ")
		if isKey == 'y':

			var = []
			keyboard = 'begin'

			for i in range(len(self.shape)):
				print(self.shape[i].info())

				while keyboard != 'done':

					keyboard = input("Which columns to remove from the dataframe? (Type 'done' to exit)    ")
					var.append(str(keyboard))

				for j in range(len(var)-1):
					self.shape[i] = self.shape[i].drop(columns=[var[j].upper])


		
	# renameColumnHeaders() - prompt the client if the would like to change any columnnames and makes the requested changes
	def renameColumn(self):

		old = []
		new = [] 
		keyboard_old = 'begin'

		isKey = input("Rename columns? (y or n)    ")
		if isKey == 'y':

			for i in range(len(self.csv)):
				print(self.csv[i].info())

				while keyboard_old != 'done':

					keyboard_old = input("Which columns to rename? (Type 'done' to exit)    ")
					
					if keyboard_old != 'done':
						keyboard_new = input("What do you want to rename " + keyboard_old + " to?    ")
						self.csv[i] = self.csv[i].rename(columns = {keyboard_old : keyboard_new})

	# dataTypeToFloat() - asks client if they would like to change the variable values to floats for analysis and
	# makes the necessary change per the client's input
	def columnToFloat(self):

		keyboard = 'begin'

		isKey = input("Change column data types to float? (y or n)    ")
		if isKey == 'y':

			for i in range(len(self.csv)):	

				while keyboard != 'done':

					print(self.csv[i].info())
					keyboard = input("Column to change to float values? (Type 'done' to exit)    ")

					if keyboard != 'done':
						self.csv[i][keyboard] = pd.to_numeric(self.csv[i][keyboard], errors='coerce')

	# StandardizeXValues() -
	def standardizeXValues(self):
		for i in range(len(self.csv)):
			keyboard = input("Do you want to standardize all X values?    (y or n)    ")
			if keyboard == 'y':
			
				y = input("What variable name is the dependent variable?    ")

				for col in self.csv[i].columns:

					if col != y:

						x_std = self.csv[i][col] - self.csv[i][col].mean() / self.csv[i][col].std()
						self.csv[i][col] = x_std


	# removeRows() - asks clients for rows to remove and gives the option of rows to remove within a range of values
	#
	def removeRows(self):
		isKey = input("Remove rows from dataframe? (y or n)    ")
		if isKey == 'y':
			
			col = 'begin'

			for i in range(len(self.csv)):
				print(self.csv[i].info())

				while col != 'done':
					
					col = input("Which column name to remove a row from? (Type 'done' to exit)    ")
					
					if col != 'done':
						value = input("What value threshold to remove?    ")
						method = input("What method to remove value? (1) >  (2) <  (3) >=  (4) <=  (5) =    ")
						if method == '1':
							
							for index, row in self.csv[i].iterrows():
								if row[col] > pd.to_numeric(value):
									self.csv[i].drop(index, inplace = True)

							print('Rows where values greater than ', value, ' from column ', col, ' removed')
							
						if method == '2':
							
							for index, row in self.csv[i].iterrows():
								if row[col] < pd.to_numeric(value):
									self.csv[i].drop(index, inplace = True)

							print('Rows where values less than ', value, ' from column ', col, ' removed')

						if method == '3':
							
							for index, row in self.csv[i].iterrows():
								if row[col] >= pd.to_numeric(value):
									self.csv[i].drop(index, inplace = True)	
							
							print('Rows where values greater than or equal to ', value, ' from column ', col, ' removed')

						if method == '4':
							
							for index, row in self.csv[i].iterrows():
								if row[col] <= pd.to_numeric(value):
									self.csv[i].drop(index, inplace = True)
							
							print('Rows where values less than or equal to ', value, ' from column ', col, ' removed')

						if method == '5':

							for index, row in self.csv[i].iterrows():
								if row[col] == pd.to_numeric(value):
									self.csv[i].drop(index, inplace = True)

							print('Rows where values equal to ', value, ' from column ', col, ' removed')


							# ind = self.csv[i][self.csv[i][col] == pd.to_numeric(value)].index[0]
							# self.csv[i] = self.csv[i].drop(self.csv[i].index[ind])	
							# print('Rows where values equal to ', value, ' from column ', col, ' removed')
					


					else:
						print('No rows removed')

				self.csv[i] = pd.DataFrame(self.csv[i])





	# spatialJoin(shape, how, join) - creates a spatial join between two shape files and stores the join in the current shapefile
	# parameters are the shapefile to be joined, how (left, right, inner), and join (intersects, within, contains)
	def spatialJoin(self, shape, how, join):
		for i in range(len(self.shape)):
			self.shape[i] = gpd.GeoDataFrame(gpd.sjoin(self.shape[i], shape, how=how, op=join))


	# leftJoinTables() - join current dataframe to new dataframe with a left join
	# parameters include a dataframe df which whill join the current dataframe
	def leftJoinTables(self, df):
		for i in range(len(self.csv)):
			print(self.csv[i].info())
			key = input("Which column header is the key value?    ")
			self.csv[i] = pd.merge(self.csv[i], df, on=key, how='left')	

	# outerJoinTables() - join current dataframe to new dataframe with a outer join
	# parameters include a dataframe df which whill join the current dataframe
	def outerJoinTables(self, df):
		for i in range(len(self.csv)):
			print(self.csv[i].info())
			key = input("Which column header is the key value?    ")
			self.csv[i] = pd.merge(self.csv[i], df, on=key, how='outer')	

	# innerJoinTables() - join current dataframe to new dataframe with a inner join
	# parameters include a dataframe df which whill join the current dataframe
	def innerJoinTables(self, df):
		for i in range(len(self.csv)):
			print(self.csv[i].info())
			key = input("Which column header is the key value?    ")
			self.csv[i] = pd.merge(self.csv[i], df, on=key, how='inner')	

	# rightJoinTables() - join current dataframe to new dataframe with a right join
	# parameters include a dataframe df to be joined to the current dataframe
	def rightJoinTables(self, df):
		for i in range(len(self.csv)):
			print(self.csv[i].info())
			key = input("Which column header is the key value?    ")
			self.csv[i] = pd.merge(self.csv[i], df, on=key, how='right')


	# leftJoinToTable() - join current shapefile attribute table to a new dataframe with a left join
	# parameters include a dataframe df to be joined to the current shapfile
	def leftJoinTableToShape(self, df):
		for i in range(len(self.shape)):
			self.shape[i]['GEOID'] = self.shape[i]['GEOID'].astype(float)
			df['GEOID'] = df['GEOID'].astype(float)
			self.shape[i] = self.shape[i].merge(df, on='GEOID')



	
	# setPointShapefile() - creates a shapefile out of point objects based on longitude and latitude
	# The dataframe is taken from the merged data (self.merge) and appended to the shape list (self.shape)
	def setPoints(self):

		for i in range(len(self.csv)):

			print(self.csv[i].info())
			
			lat = input("Variable to use as latitude: \n")
			lon = input("Variable name to use as longitude: \n")

			lat = lat.upper()
			lon = lon.upper()

			self.csv[i] = self.csv[i].rename(columns={lat : 'Latitude'})
			self.csv[i] = self.csv[i].rename(columns={lon : 'Longitude'})

			df = self.csv[i]
			df['geometry'] = df.apply(lambda x: Point((float(x.Longitude), float(x.Latitude))), axis = 1)
			crs = {'init':'epsg:4269'}
			self.shape.append(gpd.GeoDataFrame(df, crs = crs, geometry='geometry'))

	# setCRS() -
	#
	def setCRS(self):
		for i in range(len(self.shape)):
			self.shape[i].crs = {'init' :'epsg:4326'}


	# Calculate probabilities for each observed event and create a new column named as the observed + _prob
	#
	def setProbability(self):
		for i in range(len(self.csv)):

			keyboard = input("Do you want to calculate probabilities? (y or n)    ")

			if keyboard == 'y':

				print(self.csv[i].info())

				col = 'begin'

				while col != 'done':

					col = input("Which variable do you want to calculate probabilities for? (Type 'done' to exit)   ")

					if col != 'done':

						for j in range(len(self.csv)):
							prob = []

							kde = scipy.stats.gaussian_kde(self.csv[j][col])

							for k in range(0, len(self.csv[j])):
								prob.append(kde.pdf(k))

							prob = pd.DataFrame(prob)

							self.csv[i][col + '_prob'] = prob


	# Data transformations
	#
	def transformDataLogit(self):

		keyboard = input("Would you like to transform your data? (1) Log    (2) Logit    (3) None    ")

		if keyboard == '1':

			for i in range(len(self.csv)):
				print(self.csv[i].info())

				y_transf = []
				positive_vals = []
				vals = []

				data = 'begin'

				while data != 'done':

					data = input("Which variable would you like to transform? (Type 'done' to exit)    ")	

					if data != 'done':

						for j in range(0, len(self.csv[i][data])):
							vals.append(self.csv[i][data][j]/100.0)

						for j in range(0, len(vals)):
							if vals[j] > 0:
								positive_vals.append(vals[j])

						positive_vals = pd.DataFrame(positive_vals)
						minimum = (float(positive_vals.min()/2.0))

						for j in range(0, len(self.csv[i][data])):
							if vals[j] == 0.0:
								y_transf.append(minimum/2.0)
							else:
								y_transf.append(vals[j])

						for j in range(0, len(y_transf)):
							y_transf[j] = np.log(y_transf[j])

						y_transf = pd.DataFrame(y_transf)
							
						self.csv[i]['TRANSF_' + data] = y_transf  



		if keyboard == '2':

			for i in range(len(self.csv)):
				print(self.csv[i].info())

				y_transf = []
				positive_vals = []
				vals = []

				data = 'begin'

				while data != 'done':

					data = input("Which variable would you like to transform? (Type 'done' to exit)    ")	

					if data != 'done':

						for j in range(0, len(self.csv[i][data])):
							vals.append(self.csv[i][data][j]/100.0)

						for j in range(0, len(vals)):
							if vals[j] > 0:
								positive_vals.append(vals[j])

						positive_vals = pd.DataFrame(positive_vals)
						minimum = (float(positive_vals.min()/2.0))

						for j in range(0, len(vals)):
							if vals[j] == 0.0:
								y_transf.append(minimum/2.0)

							else:
								y_transf.append(vals[j])

						for j in range(0, len(y_transf)):
						 	y_transf[j] = np.log((y_transf[j]) / (1-y_transf[j]))

						y_transf = pd.DataFrame(y_transf)
							
						self.csv[i]['TRANSF_' + data] = y_transf    


# GETTER METHODS:


	# getCSV() - returns each CSV in the self.csv list
	def getDF(self):
		for i in range(len(self.csv)):
			return self.csv[i]

	# getCSV() - returns each CSV in the self.csv list
	def getShape(self):
		for i in range(len(self.shape)):
			return self.shape[i]

	# saveShapefile(filename, directory) - saves a shapefile in the parameter directory as parameter filename
	def saveShapefile(self, filename, directory):
		os.chdir(directory)
		sf = self.shape[0]
		sf.to_file(filename = filename, driver = 'ESRI Shapefile')

	# saveCSV(filename, directory) - saves a CSV in the parameter directory as parameter filename
	def saveCSV(self, filename, directory):
		os.chdir(directory)
		csv = self.csv[0]
		csv.to_csv(filename, encoding='utf-8', )








