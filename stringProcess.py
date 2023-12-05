from ReadConfig import ReadConfig
import urllib
from pathlib import Path
from EditParamTest import EditParamTest
from AddParamTest import AddParamTest
from AddCustParamTest import AddCustParamTest
from KeepParamTest import KeepParamTest
from ParamSpecificTest import ParamSpecificTest

class StringProcess():
	MAX=1000000
	ParamTypeDelete='deleteType'
	ParamTypeEdit='editType'
	ParamTypeKeep='keepType'
	ParamTypeAdd='addType'
	TestCaseName='TestCaseName'

	def __init__(self, encodedUrl):
		super(StringProcess, self).__init__()

		self.__url = encodedUrl
		self.__decoded_output_url = urllib.parse.unquote(encodedUrl)
		
		self.encodedUrl=encodedUrl.split('?')[1]
		self.decodedUrl=urllib.parse.unquote(encodedUrl.split('cust_params=')[1])

		ConfigData= ReadConfig()
		self.All_OrderedUrlParamDic = ConfigData.GetOrderedUrlParamDic()
		self.All_OrderedCustParamDic = ConfigData.GetOrderedCustParam()

		self.All_ParamTypeAndValuesDic = ConfigData.GetParamValues()
		self.All_UrlParamWithTypesAndValues = self.All_ParamTypeAndValuesDic['params']['url']
		self.All_CustParamWithTypesAndValues = self.All_ParamTypeAndValuesDic['params']['cust']

		self.__epTest = EditParamTest(encodedUrl)
		self.__addTest = AddParamTest(encodedUrl)
		self.__keepTest = KeepParamTest(encodedUrl)
		self.__addCustTest = AddCustParamTest(encodedUrl)
		self.__param_SpecTest = ParamSpecificTest(encodedUrl)

		self.url_order_ok=True
		self.cust_order_ok=True

		self.delete_url_param_exists=False
		self.delete_cust_param_exists=False

		self.add_url_param_missing=False
		self.add_cust_param_missing=False

		self.edit_url_param_missing=False
		self.edit_cust_param_missing=False

		self.keep_url_param_missing = False
		self.keep_cust_param_missing = False

		self.__paramSpec_url_param_missing=False
		self.__paramSpec_cust_param_missing=False


		self.misplaced_url_params=[]
		self.misplaced_cust_params=[]

		self.url_param_list=[]
		self.cust_param_list=[]

		self.missing_edit_url_params=[]
		self.missing_add_url_params=[]
		self.existing_delete_url_params=[]
		self.missing_keep_url_params=[]

		self.missing_add_cust_params=[]
		self.missing_edit_cust_params=[]
		self.existing_delete_cust_params=[]
		self.missing_keep_cust_params=[]
		self.paramSpec_missing_url_params=[]
		self.paramSpec_missing_cust_params=[]


		self.__expected_edit_url_params=[]
		self.__expected_edit_cust_params=[]

		self.__expected_add_url_params=[]
		self.__expected_add_cust_params=[]

		self.__expected_keep_url_params=[]
		self.__expected_keep_cust_params=[]
		#print(self.All_UrlParamWithTypesAndValues[StringProcess.ParamTypeDelete])
		#print(self.All_CustParamWithTypesAndValues[StringProcess.ParamTypeKeep])


	def CheckForParamSpecificTest(self):
		self.__param_SpecTest.CheckParamSpecificTest()
		self.__paramSpec_url_param_missing = self.__param_SpecTest.CheckAnyUrlParamMissing()
		self.__paramSpec_cust_param_missing = self.__param_SpecTest.CheckAnyCustParamMissing()

		self.paramSpec_missing_url_params = self.__param_SpecTest.GetMissingUrlParamList()
		self.paramSpec_missing_cust_params = self.__param_SpecTest.GetMissingCustParamList()

	
	def GetParamSpecificTestResult(self):
		if self.__paramSpec_url_param_missing==False and self.__paramSpec_cust_param_missing==False:
			return f"Pass\nAll the expected params are present"
		elif self.__paramSpec_url_param_missing==False and self.__paramSpec_cust_param_missing==True:
			return f"Fail\nMissing cust params are:\n{self.paramSpec_missing_cust_params}"
		elif self.__paramSpec_url_param_missing==True and self.__paramSpec_cust_param_missing==False:
			return f"Fail\nMissing url params are:\n{self.paramSpec_missing_url_params}"
		return f"Fail\nMissing url params are:\n{self.paramSpec_missing_url_params}\nMissing cust params are:\n{self.paramSpec_missing_cust_params}"

	@staticmethod
	def GetParamListWithValue(str):
		plist = str.split('&')
		return plist

	#@classmethod
	@staticmethod
	def GetParamListWithKeyOnly(str):
		plist=[]
		tmpList = str.split('&')
		for item in tmpList:
			plist.append(item.split('=')[0])
		return plist

	@staticmethod
	def CheckOrderUtil(plist:list, orderedDict:dict, orderOk:bool):
		arr=[]
		tmp=[]
		orderBreakList=[]
		for item in plist:
			if item in orderedDict.keys():
				if 'cust_params' in item:
					continue
				else:
					arr.append(orderedDict[item])
			else:
				arr.append(StringProcess.MAX)
			tmp.append(item)

		if len(arr)<=1:
			orderOk=True
			return orderBreakList

		if plist[-1]!='cust_params':
			orderOk=False
		
		for i in range(1, len(arr)):
			if arr[i]<=arr[i-1]:
				if arr[i]==StringProcess.MAX and arr[i]==arr[i-1]:
					continue
				else:
					orderOk=False
					orderBreakList.append(tmp[i])
					#return False
		return orderBreakList


	def CheckOrder(self):

		self.url_param_list = StringProcess.GetParamListWithKeyOnly(self.encodedUrl)
		arr = StringProcess.CheckOrderUtil(self.url_param_list, self.All_OrderedUrlParamDic, self.url_order_ok)
		
		if len(arr)==0:#self.url_order_ok == True:
			#print("URL params Order check: passed")
			self.url_order_ok=True
		else:
			#print("URL params Order check: failed")
			#print("Missplaced url params:")
			#print(arr)
			self.url_order_ok=False
			self.misplaced_url_params.append(arr)
		
		self.cust_param_list = StringProcess.GetParamListWithKeyOnly(self.decodedUrl)
		arr = StringProcess.CheckOrderUtil(self.cust_param_list, self.All_OrderedCustParamDic, self.cust_order_ok)

		if len(arr)==0:#self.cust_order_ok == True:
			#print("Cust params Order check passed")
			self.cust_order_ok=True
		else:
			#print("Cust params Order check failed")
			#print("Missplaced cust params:")
			#print(arr)
			self.cust_order_ok=False
			self.misplaced_cust_params.append(arr)



	@staticmethod
	def CheckDeleteParamUtil(plist:list, deleteParamList:list):
		arr=[]
		for item in deleteParamList:
			s=item.strip()
			if s in plist:
				deleteparamExists=True
				arr.append(s)

		return arr



	def CheckForDeleteParams(self):
		self.All_DeleteUrlParams = self.All_UrlParamWithTypesAndValues[StringProcess.ParamTypeDelete].split(',')
		self.All_DeleteCustParams = self.All_CustParamWithTypesAndValues[StringProcess.ParamTypeDelete].split(',')
		#print(delete_url_params)

		arr = StringProcess.CheckDeleteParamUtil(self.url_param_list, self.All_DeleteUrlParams)
		if len(arr)==0: 
			#print("Url param does not contain any delete type: passed")
			self.delete_url_param_exists=False
		else:
			#print("Url param contains delete type: failed")
			#print("params are:")
			#print(arr)
			self.delete_url_param_exists=True
			self.existing_delete_url_params=arr
			

		arr = StringProcess.CheckDeleteParamUtil(self.cust_param_list, self.All_DeleteCustParams)
		if len(arr)==0: 
			#print("cust param does not contain any delete type: passed")
			self.delete_cust_param_exists=False
		else:
			#print("cust param contains delete type: failed")
			#print("params are:")
			#print(arr)
			self.delete_cust_param_exists=True
			self.existing_delete_cust_params=arr
			

	@staticmethod
	def CheckAddParamUtil(plist:list, addParamlist:list):
		arr=[]
		for item in addParamlist:
			s=item.strip()
			if s in plist:
				continue
			else:
				arr.append(s)
		return arr


	def CheckForAddParams(self):
		self.add_url_param_missing = self.__addTest.CheckAnyAddUrlParamMissing()
		self.__expected_add_url_params = self.__addTest.GetExpectedUrlParamList()
		self.missing_add_url_params = self.__addTest.GetMissingUrlParamList()

		self.add_cust_param_missing = self.__addCustTest.CheckAnyAddCustParamMissing()
		self.__expected_add_cust_params = self.__addCustTest.GetExpectedCustParamList()
		self.missing_add_cust_params = self.__addCustTest.GetMissingCustParamList()



	@staticmethod
	def CheckEditParamUtil(plist:list, editParamlist:list):
		arr=[]
		for item in editParamlist:
			s=item.strip()
			if s in plist:
				continue
			else:
				arr.append(s)
		return arr


	def CheckForEditParams(self):
		self.edit_url_param_missing = self.__epTest.CheckAnyEditUrlParamMissing()
		self.__expected_edit_url_params = self.__epTest.GetExpectedUrlParamList()
		self.missing_edit_url_params = self.__epTest.GetMissingUrlParamList()

		self.edit_cust_param_missing = self.__epTest.CheckAnyEditCustParamMissing()
		self.__expected_edit_cust_params = self.__epTest.GetExpecteCustParamList()
		self.missing_edit_cust_params = self.__epTest.GetMissingCustParamList()


	def CheckForKeepParams(self):
		self.keep_url_param_missing = self.__keepTest.Check_KeepUrls_in_outputUrl()
		self.__expected_keep_url_params = self.__keepTest.GetExpectedUrlParamList()
		self.missing_keep_url_params = self.__keepTest.GetMissingUrlParamList()

		self.keep_cust_param_missing = self.__keepTest.Check_KeepCust_in_outputUrl()
		self.__expected_keep_cust_params = self.__keepTest.GetExpectedCustParamList()
		self.missing_keep_cust_params = self.__keepTest.GetMissingCustParamList()


	def GetUrlParamList(self, paramList:list):
		param_str=""
		for item in paramList:
			if item not in self.All_OrderedUrlParamDic.keys():
				s=item+" : Unlisted param, should be listed after all Url params except cust_params\n"
			else:
				s=item+" : "+str(self.All_OrderedUrlParamDic[item])+"\n"
			param_str+=s

		return param_str

	def GetCustParamList(self, paramList:list):
		param_str=""
		for item in paramList:
			if item not in self.All_OrderedCustParamDic:
				s=item+" : Unlisted param,should be placed after all the listed cust_params\n"
			else:
				s=item+" : "+str(self.All_OrderedCustParamDic[item])+"\n"
			param_str+=s

		return param_str

	def GetDecodedOutputUrl(self):
		return self.__decoded_output_url


	def GetUrlParamOrderTestResult(self):
		if self.url_order_ok==True:
			return "Pass"
		
		return "Fail\n"+str(self.misplaced_url_params)


	def GetCustParamOrderTestResult(self):
		if self.cust_order_ok==True:
			return "Pass"
		
		return "Fail\n"+str(self.misplaced_cust_params)


	def GetAddUrlParamTestResult(self):
		if self.add_url_param_missing==False:
			return f"Pass\nAll the expected params are present\nExpected Param list:\n{self.__expected_add_url_params}"
		
		return f"Fail\nMissing Add Url params are:\n{self.missing_add_url_params}\nExpected Param list:\n{self.__expected_add_url_params}"


	def GetEditUrlParamTestResult(self):
		if self.edit_url_param_missing==False:
			return f"Pass\nAll the expected params are present\nExpected Param list:\n{self.__expected_edit_url_params}"
		
		return f"Fail\nMissing Edit Url params are:\n{self.missing_edit_url_params}\nExpected Param list:\n{self.__expected_edit_url_params}"


	def GetKeepUrlParamTestResult(self):
		if self.keep_url_param_missing==False:
			return f"Pass\nAll the expected params are present\nExpected Param list:\n{self.__expected_keep_url_params}"
		
		return f"Fail\nMissing Keep Url params are:\n{self.missing_keep_url_params}\nExpected Param list:\n{self.__expected_keep_url_params}"


	def GetDeleteUrlParamTestResult(self):
		if self.delete_url_param_exists==False:
			return f"Pass\nAll delete type url param are missing\nFollowing params shoud not  present\n{self.All_DeleteUrlParams}"
		
		return "Fail\nAdded Delete Url params are:\n"+str(self.existing_delete_url_params)


	def GetAddCustParamTestResult(self):
		if self.add_cust_param_missing==False:
			ret_str = f"Pass\nAll exppected Add Cust params are present\n{self.__expected_add_cust_params}"
			if len(self.__expected_add_cust_params)!=self.__addCustTest.GetTotalMaxParamCount():
				ret_str = f"Pass\nAll exppected Add Cust params are present\n{self.__expected_add_cust_params}\nExcluded params are:\n{self.__addCustTest.GetExcludedCustParamList()}"
			return ret_str

		return f"Fail\nMissing Add Cust params are:\n{self.missing_add_cust_params}\nExpected Param list:\n{self.__expected_add_cust_params}"#+str(self.missing_add_cust_params)


	def GetEditCustParamTestResult(self):
		if self.edit_cust_param_missing==False:
			return f"Pass\nAll the expected params are present\nExpected Param list:\n{self.__expected_edit_cust_params}"
		
		return f"Fail\nMissing Edit cust params are:\n{self.missing_edit_cust_params}\nExpected Param list:\n{self.__expected_edit_cust_params}"

	def GetKeepCustParamTestResult(self):
		if self.keep_cust_param_missing==False:
			return f"Pass\nAll the expected params are present\nExpected Param list:\n{self.__expected_keep_cust_params}"
		
		return f"Fail\nMissing keep cust params are:\n{self.missing_keep_cust_params}\nExpected Param list:\n{self.__expected_keep_cust_params}"

	def GetDeleteCustParamTestResult(self):
		if self.delete_cust_param_exists==False:
			return f"Pass\nAll delete type cust params are missing\nFollowing params shoud not present\n{self.All_DeleteCustParams}"
		
		return "Fail\nAdded Delete Cust params are:\n"+str(self.existing_delete_cust_params)

	def GetTestCaseName(self):
		arr = (self.encodedUrl.split("cust_params=")[1]).split('%26')
		for item in arr:
			if StringProcess.TestCaseName in item:
				return item.split('%3D')[1]
		return ""



