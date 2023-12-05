from ReadConfig import ReadConfig
import urllib
from pathlib import Path

import os
import sys

current_dir = os.getcwd()
utilitydir = current_dir+"/utility"

sys.path.insert(1, utilitydir)

from InputDataReader import InputDataReader

class EditParamTest():

	FilePath = os.getcwd()+"/config/TestInput.csv"
	"""docstring for EditParamTest"""
	def __init__(self, encodedUrl):
		super(EditParamTest, self).__init__()
		self.__encodedUrl = encodedUrl
		self.__decodedUrl = urllib.parse.unquote(self.__encodedUrl)

		self.__rd = ReadConfig()
		self.__configData = self.__rd.GetParamValues()

		self.__allEditUrlParams = self.__configData['params']['url']['editType']
		self.__allEditCustParams = self.__configData['params']['cust']['editType']

		self.__allUrlParamValues = self.__configData['params']['url_values']
		self.__allCustParamValues = self.__configData['params']['cust_values']

		self.__missing_edit_cust_params=[]
		self.__missing_edit_url_params=[]

		self.__missing_any_edit_url_params = True
		self.__missing_any_cust_url_params = True

		self.__expected_edit_urls_arr = []
		self.__expected_edit_cust_arr = []


	def GetExpecteCustParamList(self):
		return self.__expected_edit_cust_arr

	def GetMissingCustParamList(self):
		return self.__expected_edit_urls_arr

	def GetExpectedUrlParamList(self):
		return self.__expected_edit_urls_arr

	def GetMissingUrlParamList(self):
		return self.__missing_edit_url_params

	def CheckAnyEditUrlParamMissing(self):
		self.EditUrlParamsWithValue()
		cnt = 0
		for item in self.__expected_edit_urls_arr:
			if item in self.__decodedUrl:
				cnt+=1
			else:
				self.__missing_edit_url_params.append(item)
		#print(str(cnt))
		if cnt==len(self.__expected_edit_urls_arr):
			self.__missing_any_edit_url_params=False
			#print("Passed url")
		else:
			self.__missing_any_edit_url_params=True
			#print("Failed url")
		return self.__missing_any_edit_url_params

	def CheckAnyEditCustParamMissing(self):
		self.EditCustParamsWithValue()
		cnt = 0
		for item in self.__expected_edit_cust_arr:
			if item in self.__decodedUrl.split('cust_params=')[1]:
				cnt+=1
			else:
				self.__missing_edit_cust_params.append(item)

		#print(str(cnt))
		if cnt==len(self.__expected_edit_cust_arr):
			self.__missing_any_edit_cust_params=False
			#print("Passed cust")
		else:
			self.__missing_any_edit_cust_params=True
			#print("Failed cust")
		return self.__missing_any_edit_cust_params

	def EditUrlParamsWithValue(self):
		arr=[]
		for it in self.__allEditUrlParams.split(','):
			isMatch=0
			for item in self.__allUrlParamValues.keys():		
				if item == it.strip():
					isMatch=1
					value = self.ExtractValue(item, self.__allUrlParamValues)
					arr.append(it.strip()+"="+value)#+self.__allUrlParamValues[item])
					#print(it.strip()+"="+self.__allUrlParamValues[item])
					break
			if isMatch==0:
				arr.append(it.strip()+"=")

		self.__expected_edit_urls_arr = arr
		return arr


	def EditCustParamsWithValue(self):
		arr=[]
		for it in self.__allEditCustParams.split(','):
			isMatch=0
			for item in self.__allCustParamValues.keys():		
				if item == it.strip():
					isMatch=1
					value = self.ExtractValue(item, self.__allCustParamValues)
					arr.append(it.strip()+"="+value)#+self.__allCustParamValues[item])
					break
			if isMatch==0:
				arr.append(it.strip()+"=")

		self.__expected_edit_cust_arr = arr


	def EditTestCustParam(self):
		arr = self.GetAllEditCustParamInReq()
		all_custParams=urllib.parse.unquote(self.__encodedUrl.split('cust_params=')[1]).split('&')
		count_edit_cust_params = 0
		
		for item in arr:
			found = 0
			for it in all_custParams:
				if str(item)==str(it):
					found=1
					break
			if found==0:
				self.__missing_edit_cust_params.append(item)
			count_edit_cust_params+=found
		print(str(count_edit_cust_params))
		if count_edit_cust_params == len(arr):
			self.__missing_any_cust_url_params = False
			print("Pass\nverified edit cust params all present with values")
		else:
			print("failed")

	def GetAllEditCustParamInReq(self):
		arr=self.__allEditCustParams.split(',')
		editCustParams=[]
		for item in arr:
			if item.strip() in self.__allCustParamValues.keys():
				s=item.strip()+"="+self.ExtractValue(item.strip(), self.__allCustParamValues)
			else:
				s=item.strip()+"="
			editCustParams.append(s)

		return editCustParams

	def EditTestUrlParam(self):
		arr = self.GetAllEditUrlParamInReq()
		all_urlParams=self.__encodedUrl.split('&')
		count_edit_url_params = 0

		for it in arr:
			found = 0
			for item in all_urlParams:
				if 'cust_params' in it:
					if 'cust_params' in item:
						found = 1
						break
					continue
				if str(it)==str(item):
					found = 1
					break
			if found==0:
				self.__missing_edit_url_params.append(item)
			count_edit_url_params+=found

		print(str(count_edit_url_params))
		if count_edit_url_params == len(arr):
			print("verified edit url params all present with values")
			self.__missing_any_edit_url_params = False
		else:
			print("failed")


	def ExtractParamValueUtil(self, param_variable, urlstr):
		arr = urlstr.split('&')
		tmp_arr=[]
		for item in arr:
			if param_variable+"=" in item:
				tmp_arr = item.split("=")

		if len(tmp_arr)>1:
			return tmp_arr[1]
		return ""

	def ExtractParamValueFromInput(self, param_variable):
		tcid = self.GetTCIDFromOutPutUrl()
		InputObj = InputDataReader(tcid, EditParamTest.FilePath)
		input_req_url = InputObj.ReadInputReq()

		url_param_part = (input_req_url.split('cust_params=')[0])#.split('?')[1]
		cust_param_part = urllib.parse.unquote(input_req_url.split('cust_params=')[1])

		v = self.ExtractParamValueUtil(param_variable, url_param_part)
		if v == "":
			return self.ExtractParamValueUtil(param_variable, cust_param_part)
		return v


	def ExtractParamValueFromOutput(self, param_variable):
		url_param_part = (self.__encodedUrl.split('cust_params=')[0]).split('?')[1]
		cust_param_part = urllib.parse.unquote(self.__encodedUrl.split('cust_params=')[1])

		v = self.ExtractParamValueUtil(param_variable, url_param_part)
		if v == "":
			return self.ExtractParamValueUtil(param_variable, cust_param_part)
		return v

	def EvaluateParamValue(self, param_variable):
		if param_variable.strip() in self.__allUrlParamValues.keys():
			return self.__allUrlParamValues[param_variable.strip()]

		if param_variable.strip() in self.__allUrlParamValues.keys():
			return self.__allCustParamValues[param_variable.strip()]

		return self.ExtractParamValueFromOutput(param_variable)


	def ExtractValue(self, key, dic):
		s = dic[key]
		if '<<' in s:
			param_variable = s.split('<<')[1].replace('>>','')
			value = self.EvaluateParamValue(param_variable)
			
			if value==None:
				s = s.split('<<')[0]
			else:
				s = s.split('<<')[0]+str(value)
		return s


	def GetAllEditUrlParamInReq(self):
		arr=self.__allEditUrlParams.split(',')
		editUrlParams=[]
		for item in arr:
			if item.strip() in self.__allUrlParamValues.keys():
				s=item.strip()+"="+self.ExtractValue(item.strip(), self.__allUrlParamValues)
			else:
				s=item.strip()+"="
			editUrlParams.append(s)
			
		return editUrlParams

	def TestForEditCustParam(self):
		arr=self.__allEditCustParams.split(',')
		editCustParams=[]
		for item in arr:
			if item.strip() in self.__allCustParamValues.keys():
				s=item.strip()+"="+self.ExtractValue(item.strip(), self.__allCustParamValues)
			else:
				s=item.strip()+"="
			editCustParams.append(s)
			
		return editCustParams

		
	def Decode(self, url):
		return urllib.parse.unquote(url)

	def GetTCIDFromOutPutUrl(self):
		#decodedUrl = self.Decode(self.__encodedUrl)
		try:

			custParams = self.__encodedUrl.split('cust_params')[1]
			custParams=custParams.replace('cust_params', '')
			params = custParams.split("%26")
			tcid=""
			for item in params:
				if 'TCID' in item:
					tcid = item.split("%3D")[1]
					break

			return tcid.strip()
		except:
			print("TcID not found")

	def GetUrlParamValue_fromInputUrl(urlParam):
		pass


	def GetCustParamValue_fromInputUrl(custParam):
		pass

	def disPlay(self):
		print(self.__expected_edit_cust_arr)
		print(self.__expected_edit_urls_arr)


url='http://kayo-gam-proxy-perf/gampad/live/ads?path=Upath&ss_req=Uss_req&env=Uenv&gdfp_req=Ugdfp_req&unviewed_position_start=Uunviewed_position_start&impl=Uimpl&sz=Usz&vad_type=Uvad_type&iu=/21783347309/espn.au/kayo/Tdevice_type&pp=Upp&tfcd=Utfcd&output=xml_vast3&ad_rule=Uad_rule&cmsid=Ucmsid&vid=Uvid&ssss=Ussss&correlator=Ucorrelator&ppid=Uppid&url=Uurl&description_url=http://www.espn.com/video&scor=Uscor&mridx=Umridx&pod=Upod&npa=Unpa&is_lat=Uis_lat&rdid=Urdid&idtype=Uidtype&min_ad_duration=Umin_ad_duration&ip=Uip&vpos=Uvpos&pmnd=Upmnd&pmxd=Upmxd&pmad=Upmad&user_agent=Uuser_agent&msid=Umsid&an=Uan&cors=2023-03-14%2020:49:19.339297&cust_params=series%3DTseries%26sp%3DTsp%26chan%3DTchan%26vdm%3Dlive%26authp%3DTauthp%26plt%3DTplt%26vps%3DTvps%26adPod%3DTadPod%26ppid%3DTppid%26refDomain%3DTrefDomain%26distAssetId%3DTdistAssetId%26bundleId%3DTbundleId%26isDnt%3DTisDnt%26linearProvider%3Despn2%26metadata_sport%3DTmetadata_sport%26dph%3DTdph%26sportSeriesName%3Dmotor_Get_Up_%26metadata_live%3DTmetadata_live%26device_os%3DTdevice_os%26device_type%3DTdevice_type%26metadata_assetId%3DTmetadata_assetId%26metadata_contenttype%3DTmetadata_contenttype%26metadata_state%3DTmetadata_state%26metadata_suburb%3DTmetadata_suburb%26metadata_title%3DTmetadata_title%26metadata_woId%3D222222%26excl_cat%3Dgambling%2Codds%26TestCaseName%3DParam_Order_Test_1%26teamA%3DSRH%26teamB%3DBOS%26sportFixtureId%3Dmotor_6792%26TCID%3D1'
st = EditParamTest(url)
#st.EditUrlParamsWithValue()
#st.EditCustParamsWithValue()

#st.disPlay()

st.CheckAnyEditUrlParamMissing()
st.CheckAnyEditCustParamMissing()

#st.EditTestUrlParam()
#st.EditTestCustParam()


