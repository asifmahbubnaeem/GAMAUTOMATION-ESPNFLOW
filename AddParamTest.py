import urllib
from pathlib import Path
from ReadConfig import ReadConfig
import os
import sys
current_dir = os.getcwd()
utilitydir = current_dir+"/utility"

sys.path.insert(1, utilitydir)

from InputDataReader import InputDataReader


class AddParamTest(object):
	"""docstring for AddParamTest"""
	FilePath = os.getcwd()+"/config/TestInput.csv"
	def __init__(self, encodedUrl):
		super(AddParamTest, self).__init__()
		self.__encodedUrl = encodedUrl
		self.__decodedUrl = urllib.parse.unquote(self.__encodedUrl)

		self.__rd = ReadConfig()
		self.__configData = self.__rd.GetParamValues()

		self.__allAddUrlParams = self.__configData['params']['url']['addType'].split(',')
		self.__allAddCustParams = self.__configData['params']['cust']['addType'].split(',')


		self.__allUrlParamValues = self.__configData['params']['url_values']
		self.__allCustParamValues = self.__configData['params']['cust_values']

		self.__expected_add_url_param_list = []
		self.__expected_add_cust_param_list = []

		self.__input_req = ""

		self.__missing_any_add_url_params = True

		self.__missing_add_url_param_list = []



	def GetExpectedUrlParamList(self):
		return self.__expected_add_url_param_list

	def GetMissingUrlParamList(self):
		return self.__missing_add_url_param_list

	def CheckAnyAddUrlParamMissing(self):
		self.AddUrlParamsWithValue()
		cnt = 0
		for item in self.__expected_add_url_param_list:
			if item in self.__decodedUrl:
				cnt+=1
			else:
				self.__missing_add_url_param_list.append(item)
		#print(str(cnt))
		if cnt==len(self.__expected_add_url_param_list):
			self.__missing_any_add_url_params=False
			#print("Passed url")
		else:
			self.__missing_any_add_url_params=True
			#print("Failed url")
		return self.__missing_any_add_url_params

	def ParamValueInConfig(self, param, paramType):
		if paramType == 'url':
			for item in self.__allUrlParamValues.keys():
				if param in item and item in param:
					return self.__allUrlParamValues[param]

		elif paramType == 'cust':
			for item in self.__allCustParamValues.keys():
				if param in item and item in param:
					return self.__allCustParamValues[param]


	def GetTCIDFromOutPutUrl(self):
		try:

			custParams = self.__encodedUrl.split('cust_params')[1]
			custParams=custParams.replace('cust_params=', '')
			params = custParams.split("%26")
			tcid=""
			for item in params:
				if 'TCID' in item:
					tcid = item.split("%3D")[1]
					break

			return tcid.strip()
		except:
			print("TcID not found")


	def ParamValueInReq(self, param, paramType):
		if paramType == 'url':
			url_param_part = (self.__input_req.split('?')[1]).split('&')

			for item in url_param_part:
				if param+"=" in item:
					return item.split('=')[1]

		elif paramType == 'cust':
			pass


	def IsDefinedInReq(self, param, paramType):
		if paramType == 'url':
			tcid = self.GetTCIDFromOutPutUrl()
			if tcid=="":
				print("tcid not found")
				return
			InputObj = InputDataReader(tcid, AddParamTest.FilePath)
			input_req_url = InputObj.ReadInputReq()

			self.__input_req = input_req_url

			if param+"=" in input_req_url:
				return True
			return False
		elif paramType == 'cust':
			pass

# If add type params has any value define in input request then in the output url it would show the same value
# otherwise it show the value defined in the param_value_config.yml
# sometimes this value can be expressed in the form of another value, like plt: <<cust_params.device_type>> or bundleId: <<msid>>, in these cases 
# if cust_params.device_type or msid has any value defined in input request then it would show that value 
	def AddUrlParamsWithValue(self):
		arr=[]
		for item in self.__allAddUrlParams:
			value = ""
			if self.IsDefinedInReq(item.strip(), 'url')==True:
				value = self.ParamValueInReq(item.strip(), 'url')
			else:
				value = self.ParamValueInConfig(item.strip(), 'url')

			if value == None:
				s = item.strip()+"="
				
			else:
				s = item.strip()+"="+str(value)
				
			arr.append(s)
			self.__expected_add_url_param_list = arr

	def display(self):
		self.AddUrlParamsWithValue()
		print(self.__expected_add_url_param_list)


url='http://kayo-gam-proxy-perf/gampad/live/ads?path=Upath&ss_req=Uss_req&env=Uenv&gdfp_req=Ugdfp_req&unviewed_position_start=Uunviewed_position_start&impl=Uimpl&sz=Usz&vad_type=Uvad_type&iu=/21783347309/espn.au/kayo/Tdevice_type&pp=Upp&tfcd=Utfcd&output=xml_vast3&ad_rule=Uad_rule&cmsid=Ucmsid&vid=Uvid&ssss=Ussss&correlator=Ucorrelator&ppid=Uppid&url=Uurl&description_url=http://www.espn.com/video&scor=Uscor&mridx=Umridx&pod=Upod&npa=Unpa&is_lat=Uis_lat&rdid=Urdid&idtype=Uidtype&min_ad_duration=Umin_ad_duration&ip=Uip&vpos=Uvpos&pmnd=Upmnd&pmxd=Upmxd&pmad=Upmad&user_agent=Uuser_agent&msid=Umsid&an=Uan&cors=2023-03-14%2020:49:19.339297&cust_params=series%3DTseries%26sp%3DTsp%26chan%3DTchan%26vdm%3Dlive%26authp%3DTauthp%26plt%3DTplt%26vps%3DTvps%26adPod%3DTadPod%26ppid%3DTppid%26refDomain%3DTrefDomain%26distAssetId%3DTdistAssetId%26bundleId%3DTbundleId%26isDnt%3DTisDnt%26linearProvider%3Despn2%26metadata_sport%3DTmetadata_sport%26dph%3DTdph%26sportSeriesName%3Dmotor_Get_Up_%26metadata_live%3DTmetadata_live%26device_os%3DTdevice_os%26device_type%3DTdevice_type%26metadata_assetId%3DTmetadata_assetId%26metadata_contenttype%3DTmetadata_contenttype%26metadata_state%3DTmetadata_state%26metadata_suburb%3DTmetadata_suburb%26metadata_title%3DTmetadata_title%26metadata_woId%3D222222%26excl_cat%3Dgambling%2Codds%26TestCaseName%3DParam_Order_Test_1%26teamA%3DSRH%26teamB%3DBOS%26sportFixtureId%3Dmotor_6792%26TCID%3D1'
#st = AddParamTest(url)
#st.CheckAnyAddUrlParamMissing()
#print(str(st.GetExpectedUrlParamList()))
#print(str(st.GetMissingUrlParamList()))


