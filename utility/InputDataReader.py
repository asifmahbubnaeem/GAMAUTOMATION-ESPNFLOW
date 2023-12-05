import csv
import os
from CsvHandler import CsvHandler


class InputDataReader(object):

	InputUrlColumn = 2
	WOIDColumn = 3
	SprotColumn = 4
	CompTextColumn = 5
	ExpectedUrlParamColumn = 6
	ExpectedCustParamColumn = 7
	"""docstring for InputDataReader"""
	def __init__(self, TCID, FilePath):
		super(InputDataReader, self).__init__()
		self.__TCID = TCID
		
		current_dir = os.getcwd()
		parent_dir = os.path.dirname(current_dir)
		self.__InputRequestFilePath = FilePath


	def ReadInputReq(self):
		try:
			csvHandler = CsvHandler(self.__InputRequestFilePath)
			arr  = csvHandler.CsvRead()
			return arr[int(self.__TCID)][InputDataReader.InputUrlColumn]
		except Exception as e:
			#logger.error
			print("an exception: "+str(e))

	def GetSportsInfo(self):
		try:
			csvHandler = CsvHandler(self.__InputRequestFilePath)
			arr  = csvHandler.CsvRead()
			sports={}
			
			col_count = len(arr[int(self.__TCID)])
			if InputDataReader.WOIDColumn>col_count-1:
				sports['WOID']= ""
			else:
				sports['WOID']= arr[int(self.__TCID)][InputDataReader.WOIDColumn]

			if InputDataReader.SprotColumn>col_count-1:
				sports['Sport']= ""
			else:
				sports['Sport']= arr[int(self.__TCID)][InputDataReader.SprotColumn]
				
			if InputDataReader.CompTextColumn>col_count-1:
				sports['CompetitionText']= ""
			else:
				sports['CompetitionText']= arr[int(self.__TCID)][InputDataReader.CompTextColumn]
			return sports
		except Exception as e:
			#logger.error
			print(f"For TCID {self.__TCID} : InputDataReader.GetSportsInfo() method, exception: {str(e)}")

	def GetExpectedUrlColum(self):
		try:
			csvHandler = CsvHandler(self.__InputRequestFilePath)
			arr  = csvHandler.CsvRead()
			col_count = len(arr[int(self.__TCID)])

			if InputDataReader.ExpectedUrlParamColumn>col_count-1:
				return []
			elif arr[int(self.__TCID)][InputDataReader.ExpectedUrlParamColumn]==None:
				return []
			elif arr[int(self.__TCID)][InputDataReader.ExpectedUrlParamColumn]=="":
				return []
			return arr[int(self.__TCID)][InputDataReader.ExpectedUrlParamColumn].split( )
		except Exception as e:
			print(f"For TCID {self.__TCID} : InputDataReader.GetExpectedUrlColum() method, exception: {str(e)}")

	def GetExpectedCustColum(self):
		try:
			csvHandler = CsvHandler(self.__InputRequestFilePath)
			arr  = csvHandler.CsvRead()
			col_count = len(arr[int(self.__TCID)])

			if InputDataReader.ExpectedCustParamColumn>col_count-1:
				return []
			else:
				return arr[int(self.__TCID)][InputDataReader.ExpectedCustParamColumn].split( )
		except Exception as e:
			print(f"For TCID {self.__TCID} : InputDataReader.GetExpectedCustColum() method, exception: {str(e)}")

#id = InputDataReader(2)
#print(id.ReadInputReq())