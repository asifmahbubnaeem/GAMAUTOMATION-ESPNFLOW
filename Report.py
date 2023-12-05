import csv
#from stringProcess import StringProcess
import os
from datetime import datetime
class Report():
	"""docstring for Report"""
	
	def __init__(self, dataList:list):
		#super(Report, self).__init__()
		#self.obj_StringProcess = obj_StringProcess
		
		self.data=dataList
		self.ReportFileName='Report_'+str(datetime.now())+'.csv'
		self.InputRequest=os.getcwd()+'/config/TestInput.csv'


	def generateCSVFile(self, fileName:str):
		with open(fileName, 'w') as f:
			writer = csv.writer(f)
			for row in self.data:
				writer.writerow(row)

	def generateReport(self):
		self.generateCSVFile(self.ReportFileName)
		print("Report Generated:\n"+self.ReportFileName)


	def generateInputRequestFile(self):
		self.generateCSVFile(self.InputRequest)
		#print("Input Request File Generated:\n"+self.InputRequest)
		
		