from ReadConfig import ReadConfig
import random

class RandomOrderGen():
	def __init__(self, cors, TCID, TestCase):
		super(RandomOrderGen, self).__init__()
		Config=ReadConfig()
		ALL_Url_Param_Dic = Config.GetOrderedUrlParamDic()
		ALL_Cust_Param_Dic = Config.GetOrderedCustParam()

		self.__all_random_order_url_params = []
		for item in ALL_Url_Param_Dic.keys():
			self.__all_random_order_url_params.append(item)

		self.__all_random_order_url_params.append(cors)

		self.__all_random_order_cust_params = []
		for item in ALL_Cust_Param_Dic.keys():
			self.__all_random_order_cust_params.append(item)

		self.__all_random_order_cust_params.append("TCID%3D"+str(TCID))
		self.__all_random_order_cust_params.append("TestCaseName%3D"+TestCase + "-" +str(TCID))
		
		random.shuffle(self.__all_random_order_url_params)
		random.shuffle(self.__all_random_order_cust_params)

	def GetRandomOrderUrlParams(self):
		return self.__all_random_order_url_params

	def GetRandomOrderCustParams(self):
		return self.__all_random_order_cust_params



class RandomNumberOfParams():
	def __init__(self, cors, TCID, TestCase):
		super(RandomNumberOfParams, self).__init__()

		Config=ReadConfig()
		ALL_Url_Param_Dic = Config.GetOrderedUrlParamDic()
		ALL_Cust_Param_Dic = Config.GetOrderedCustParam()

		self.__url_params = []
		for item in ALL_Url_Param_Dic.keys():
			if 'cust_params' in item:
				self.__url_params.append(item)
			elif random.randint(0,1)==0:
				self.__url_params.append(item)

		self.__url_params.append(cors)

		self.__cust_params = []
		for item in ALL_Cust_Param_Dic.keys():
			if 'linearProvider' in item:
				self.__cust_params.append(item)
			elif 'woId' in item:
				self.__cust_params.append(item)
			elif random.randint(0,1)==0:
				self.__cust_params.append(item)

		self.__cust_params.append("TCID%3D"+str(TCID))
		self.__cust_params.append("TestCaseName%3D"+TestCase + "-" +str(TCID))

		random.shuffle(self.__url_params)
		random.shuffle(self.__cust_params)

	def GetUrlParams(self):
		return self.__url_params

	def GetCustParams(self):
		return self.__cust_params

