import yaml
from pathlib import Path
import os


#from order_check import OrderCheck 


class ReadConfig():
	DirecotryPath=os.getcwd()+"/config/"

	def __init__(self):
		self.__url_param_config_file = ReadConfig.DirecotryPath+"url_param_config.yml"     #os.getcwd()+"/config/url_param_config.yml"
		self.__cust_param_config_file= ReadConfig.DirecotryPath+"cust_param_config.yml"    #os.getcwd()+"/config/cust_param_config.yml"
		self.__param_value_config_file= ReadConfig.DirecotryPath+"param_value_config.yml"

		#self.__param_values

	def GetOrderedUrlParamDic(self):
		return yaml.safe_load(Path(self.__url_param_config_file).read_text())

	def GetOrderedCustParam(self):
		return yaml.safe_load(Path(self.__cust_param_config_file).read_text())

	def GetParamValues(self):
		return yaml.safe_load(Path(self.__param_value_config_file).read_text())

#od=OrderCheck(url_dict)
#od.display()
#arr=[]
#for key in url_dict:
#	arr.append(key)
