import urllib
from pathlib import Path
from ReadConfig import ReadConfig
import os
import sys
import json
current_dir = os.getcwd()
utilitydir = current_dir+"/utility"

sys.path.insert(1, utilitydir)

from InputDataReader import InputDataReader

class AddCustParamTest(object):
	FilePath = os.getcwd()+"/config/TestInput.csv"
	"""docstring for AddCustParamTest"""
	def __init__(self, encodedUrl):
		super(AddCustParamTest, self).__init__()
		self.__encodedUrl = encodedUrl

		self.__decodedUrl = urllib.parse.unquote(self.__encodedUrl)
		self.__TestCaseName = ""

		self.__rd = ReadConfig()
		self.__configData = self.__rd.GetParamValues()

		self.__allAddCustParams = self.__configData['params']['cust']['addType'].split(',')
		self.__total_custParams = len(self.__allAddCustParams)

		self.__allCustParamValues = self.__configData['params']['cust_values']

		self.__expected_add_cust_param_list=[]
		self.__missing_add_cust_param_list=[]
		self.__xcluded_cust_param_list = []

		self.__missing_any_add_cust_params = True

		self.__TCId = None


	def GetTCIDFromOutPutUrl(self):
		try:

			custParams = self.__encodedUrl.split('cust_params')[1]
			custParams=custParams.replace('cust_params=', '')
			params = custParams.split("%26")
			tcid=""
			for item in params:
				if 'TCID' in item:
					tcid = item.split("%3D")[1]
					self.__TCId = tcid
					break

			return tcid.strip()
		except:
			print("TcID not found")


	def IsDefinedInReq(self, param, paramType):
		if paramType == 'cust':
			tcid = self.GetTCIDFromOutPutUrl()
			#print(tcid)
			if tcid=="":
				print("tcid not found")
				return

			#print(os.path.exists(AddCustParamTest.FilePath))https://foxsportsau.atlassian.net/browse/CONTENT-2485
			InputObj = InputDataReader(tcid, AddCustParamTest.FilePath)
			input_req_url = InputObj.ReadInputReq()

			self.__input_req = input_req_url
			#print(self.__input_req)
			if param+"%3D" in input_req_url:
				return True
			return False


	def ParamValueInReq(self, param, paramType):
		cust_param_part = ""
		if paramType == 'cust':
			tmp_arr = (self.__input_req.split('?')[1]).split('&')
			for item in tmp_arr:
				if 'cust_params=' in item:
					cust_param_part = item.replace('custParams=','')
					break

			cust_param_list = cust_param_part.split('%26')
			for item in cust_param_list:
				if param+'%3D' in item:
					return item.split('%3D')[1]


	def FindParamValueInOutput_custParam(self, param):
		cust_param_str = self.__decodedUrl.split('?')[1].split('cust_params=')[1]
		#print(cust_param_str)
		custParams_arr = cust_param_str.split('&')
		#print(param+"\t"+str(custParams_arr))
		for item in custParams_arr:
			item_key = item.split('=')[0]
			if item_key == param:
				return item.replace(param,'').replace('=','')
		#return ""

	def FindParamValueInOutput_UrlParam(self, param):
		url_param_list = self.__encodedUrl.split('?')[1].split('&')

		for item in url_param_list:
			item_key = item.split('=')[0]
			if param == item_key:
				return item.replace(param,'').replace('=','')
		#print("Not found in output")
		return None

	def DeriveValue(self, pValue):
		if '<<' not in pValue:
			return pValue

		if 'cust_params.' in pValue:
			mapped_custParam = pValue.replace('<<cust_params.','').replace('>>','')
			return self.FindParamValueInOutput_custParam(mapped_custParam)
		mapped_urlParam=pValue.replace('<<','').replace('>>','')
		return self.FindParamValueInOutput_UrlParam(mapped_urlParam)


	def ParamValueInConfig(self, param, paramType):
		value=""
		if paramType == 'cust':
			for item in self.__allCustParamValues.keys():
				if param in item and item in param:
					value = self.__allCustParamValues[param]
					break
		#print(value)
		if '<<' in value and '>>' in value:
			return self.DeriveValue(value)

		return value


	def AddCustParamsWithValue(self):
		arr=[]
		for item in self.__allAddCustParams:
			value = ""
			exclude = 0
			s = ""
			if self.IsDefinedInReq(item.strip(), 'cust')==True:
				value = self.ParamValueInReq(item.strip(), 'cust')
				#print(item.strip()+"="+str(value))
			else:
				value = self.ParamValueInConfig(item.strip(), 'cust')
				if value=="":
					value=None

			if value == None:
				s = item.strip()#+"%3D"
				#print("excluded = "+item)
				exclude = 1
			else:
				s = item.strip()+"%3D"+str(value)
				exclude = 0
			
			if exclude==0:
				arr.append(s)


		self.__expected_add_cust_param_list = arr

	def GetTestCaseName(self):
		try:
			custParams = self.__encodedUrl.split('cust_params=')[1]
			custParams=custParams.replace('cust_params=', '')
			params = custParams.split("%26")
			#print(params)
			tc_name=""
			for item in params:
				if 'TestCaseName' in item:
					tc_name = item.split("%3D")[1]
					break
			self.__TestCaseName = tc_name
			return self.__TestCaseName.strip()
		except:
			print("TestCaseName not found")

	def DecodeParams(self, cust_param_list):
		arr=[]

		for item in cust_param_list:
			tmp = urllib.parse.unquote(item)
			arr.append(tmp)
		return arr

	def CheckAnyAddCustParamMissing(self):
		self.GetTestCaseName()
		self.AddCustParamsWithValue()
		cnt = 0

		compare_list=[]
		if 'specialChar' in self.__TestCaseName:
			self.__expected_add_cust_param_list = self.DecodeParams(self.__expected_add_cust_param_list)
			compare_list = self.__decodedUrl
		else:
			compare_list = self.__encodedUrl

		for item in self.__expected_add_cust_param_list:
			if item in compare_list:#self.__encodedUrl:
				cnt+=1
			else:
				self.__missing_add_cust_param_list.append(item)
		#print(str(cnt))
		if cnt==len(self.__expected_add_cust_param_list):
			self.__missing_any_add_cust_params=False
			#print("Passed url")
		else:
			self.__missing_any_add_cust_params=True
			#print("Failed url")
		return self.__missing_any_add_cust_params


	def GetMissingCustParamList(self):
		return self.__missing_add_cust_param_list

	def GetExpectedCustParamList(self):
		return self.__expected_add_cust_param_list

	def GetTCID(self):
		return self.__TCId

	def GetUrl(self):
		return self.__encodedUrl

	def GetTotalMaxParamCount(self):
		return int(self.__total_custParams)

	def ExclusionReason(self, param):
		param_value_in_config = self.__allCustParamValues[param]
		defineInReq:bool = self.IsDefinedInReq(param,'cust')

		if defineInReq == True:
			#self.__missing_any_add_cust_params = True
			return f"{param} should not be excluded"

		if param_value_in_config == None and defineInReq==False:
			return f"{param} is not defined in input url and it is not mapped to any value or param in config"

		if param_value_in_config != "":
			if '<<' not in param_value_in_config:
				#self.__missing_any_add_cust_params = True
				return f"{param}: {param_value_in_config} should not be excluded"

			if 'cust_params' in param_value_in_config:
				return f"{param_value_in_config} not defined in input/output url cust_params and {param} is excluded from input"#then {param}:{param_value_in_config} should be excluded


			return f"{param_value_in_config} and {param} are not defined"
		return "Could be a bug, pls check input/output urls"

	
	def ExcludedCustParamList(self):
		if self.__total_custParams!=len(self.__expected_add_cust_param_list):
			for item in self.__allAddCustParams:
				s = item.strip()
				found = 0
				for item2 in self.__expected_add_cust_param_list:
					t = item2.split('%3D')[0]
					if s == t:
						found = 1
						break
				if found == 0:
					reason_of_exclusion = self.ExclusionReason(item.strip())
					self.__xcluded_cust_param_list.append(f"{item.strip()} is excluded for: {reason_of_exclusion}")

	def GetExcludedCustParamList(self):
		self.ExcludedCustParamList()
		return self.__xcluded_cust_param_list


def __test():
	with open('Response.json', 'r') as f:
		data=json.load(f)
		hits=data['rawResponse']['hits']['hits']
		length=len(hits)

		for item in hits:
			url = item['_source']['url']
			st = AddCustParamTest(url)
			ret = st.CheckAnyAddCustParamMissing()
			if ret==False:
				print("pass")
				#print(f"{st.GetTCID()}\t{st.GetExpectedCustParamList()}")
			else:
				print("fail")
				print(f"{st.GetTCID()}\t{st.GetMissingCustParamList()}")
			print(f"Excluded param list:\n{st.GetExcludedCustParamList()}")
			#st.AddCustParamsWithValue()
		print(len(hits))
#__test()

def __test2():
	url = 'http://kayo-gam-proxy-perf/gampad/live/ads?path=Rand&ss_req=Rand&env=Rand&gdfp_req=Rand&unviewed_position_start=Rand&sz=Rand&vad_type=Rand&iu=/21783347309/espn.au/kayo/&pp=Rand&tfcd=Rand&output=xml_vast3&cmsid=2497009&vid=espnvod_default_asset&ssss=mediatailor&correlator=Rand&url=Rand&description_url=http://www.espn.com/video&npa=Rand&rdid=Rand&idtype=Rand&min_ad_duration=Rand&pmnd=Rand&pmxd=Rand&user_agent=Rand&cors=2023-03-2015:38:44.858481&cust_params=series%3Dmotor_Get_Up_%26chan%3Dfoxtel%26vdm%3Dlive%26authp%3DRand%26vps%3DRand%26refDomain%3DRand%26distAssetId%3DRand%26isDnt%3DRand%26linearProvider%3Despn1%26sportSeriesName%3Dmotor_Get_Up_%26metadata_live%3DRand%26device_os%3DRand%26metadata_assetId%3DRand%26metadata_contenttype%3DRand%26metadata_state%3DRand%26metadata_title%3DRand%26metadata_woId%3D222222%26excl_cat%3Dgambling%2Codds%26TestCaseName%3DParam_Order_Test_22%26TCID%3D22%26teamA%3DSRH%26teamB%3DBOS%26sportFixtureId%3Dmotor_679'
	st = AddCustParamTest(url)
	ret = st.CheckAnyAddCustParamMissing()
	if ret==False:
		print(f"{st.GetTCID()}\t{st.GetExpectedCustParamList()}\n{st.GetUrl()}")
	else:
		print(str(st.GetMissingCustParamList()) + "\ttcID = "+st.GetTCIDFromOutPutUrl())
	#st.AddCustParamsWithValue()


#__test2()



