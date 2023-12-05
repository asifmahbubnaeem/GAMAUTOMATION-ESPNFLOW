import csv


class CsvHandler(object):
	"""docstring for CsvHandler"""
	def __init__(self, FilePath:str):
		super(CsvHandler, self).__init__()
		self.__filePath = FilePath


	def CsvRead(self):
		arr=[]
		with open(self.__filePath, 'r') as f:
			csv_reader = csv.reader(f, delimiter=',')
			for row in csv_reader:
				arr.append(row)

		return arr
