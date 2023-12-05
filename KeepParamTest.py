import urllib
from pathlib import Path
from ReadConfig import ReadConfig
import json
import os
import sys
import re
current_dir = os.getcwd()
utilitydir = current_dir+"/utility"

sys.path.insert(1, utilitydir)

from InputDataReader import InputDataReader

class KeepParamTest(object):
	"""docstring for KeepParamTest"""
	FilePath = os.getcwd()+"/config/TestInput.csv"
	def __init__(self, encodedUrl):
		super(KeepParamTest, self).__init__()
		self.__encodedUrl = encodedUrl
		self.__decodedUrl = urllib.parse.unquote(self.__encodedUrl)

		self.__rd = ReadConfig()
		self.__configData = self.__rd.GetParamValues()

		self.__InputObj = None
		self.__sportsInfo = None

		self.__allKeepUrlParams = self.__configData['params']['url']['keepType'].split(',')
		self.__allKeepCustParams = self.__configData['params']['cust']['keepType'].split(',')

		self.__missing_keep_url_param=[]
		self. __missing_keep_cust_param=[]

		self.__keepUrl_list_in_input=[]
		self.__keepCust_list_in_input=[]

		self.__missing_any_keep_url_params = True
		self.__missing_any_keep_cust_params = True

		self.__executed_once = False
		#print(self.__allKeepUrlParams)
		#print(self.__allKeepCustParams)


	def GetExpectedUrlParamList(self):
		return self.__keepUrl_list_in_input

	def GetExpectedCustParamList(self):
		return self.__keepCust_list_in_input

	def GetMissingUrlParamList(self):
		return self.__missing_keep_url_param

	def GetMissingCustParamList(self):
		return self.__missing_keep_cust_param

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

	def GetInputUrl(self):
		tcid = self.GetTCIDFromOutPutUrl()
		self.__InputObj = InputDataReader(tcid, KeepParamTest.FilePath)
		input_req_url = self.__InputObj.ReadInputReq()
		return input_req_url

	def GetSportsInfo(self):
		if self.__InputObj==None:
			self.__InputObj = InputDataReader(self.GetTCIDFromOutPutUrl(),KeepParamTest.FilePath)

		self.__sportsInfo = self.__InputObj.GetSportsInfo()

	def GetSportSeriesName(self):
		if self.__sportsInfo == None:
			return ""

		sportname = self.__sportsInfo['Sport']#.replace(' ','_').replace('!','_')
		comptext = self.__sportsInfo['CompetitionText']#.replace(' ','_').replace("!", '_')
		
		sportname = re.sub('[ !@#$^()|+~-]','_',sportname)
		comptext = re.sub('[ !@#$^()|+~-]','_', comptext)

		return sportname+'_'+comptext

	def ValueInSportsInfo(self):
		if self.__sportsInfo==None:
			return False
		if self.__sportsInfo['CompetitionText']==None or self.__sportsInfo['CompetitionText']=="":
			return False
		return True

	def KeepTypeParamsIn_InputRq(self):

		if self.__executed_once==True:
			return
		self.__executed_once = True

		input_url = self.GetInputUrl()
		param_part = input_url.split('?')[1]
		url_params = param_part.split('&')
		
		for item in self.__allKeepUrlParams:
			for it in url_params:
				s = (it.split('=')[0]).strip()
				if item.strip() in s and s in item.strip():
					self.__keepUrl_list_in_input.append(it)
					break

		
		cust_param_str = ""
		for item in url_params:
			if 'cust_params=' in item:
				cust_param_str = item
				break

		cust_params = urllib.parse.unquote(cust_param_str).split('&')
		if self.__sportsInfo == None:
			self.GetSportsInfo()

		for item in self.__allKeepCustParams:
			if item.strip()=='sportSeriesName' and self.ValueInSportsInfo()==True:
				self.__keepCust_list_in_input.append(item.strip()+"="+self.GetSportSeriesName())
				continue
			for it in cust_params:
				s = (it.split('=')[0]).strip()
				if item.strip() in s and s in item.strip():
					self.__keepCust_list_in_input.append(it)

		#return keepUrl_list_in_input





	def Check_KeepUrls_in_outputUrl(self):
		self.KeepTypeParamsIn_InputRq()
		output_url_params = (self.__encodedUrl.split('?')[1]).split('cust_params')[0]

		#print(output_url_params)

		for item in self.__keepUrl_list_in_input:
			if item.strip() not in output_url_params:
				self.__missing_keep_url_param.append(item)

		if len(self.__missing_keep_url_param)==0:
			self.__missing_any_keep_url_params = False
			#print("keep url pass")
		else:
			self.__missing_any_keep_url_params = True
			#print(f"keep url Failed\n{self.__missing_keep_url_param}")
		return self.__missing_any_keep_url_params


	def Check_KeepCust_in_outputUrl(self):
		self.KeepTypeParamsIn_InputRq()
		output_cust_params = (self.__encodedUrl.split('?')[1]).split('cust_params=')[1]
		decoded_output_cust_params = urllib.parse.unquote(output_cust_params)

		for item in self.__keepCust_list_in_input:
			if item.strip() not in decoded_output_cust_params:
				self.__missing_keep_cust_param.append(item)

		if len(self.__missing_keep_cust_param)==0:
			self.__missing_any_keep_cust_params = False
			#print("keep cust pass")
		else:
			self.__missing_any_keep_cust_params = True
			#print(f"keep cust Failed\n{self.__missing_keep_cust_param}")
		return self.__missing_any_keep_cust_params

	def TestKeepTypeParams(self):
		self.KeepTypeParamsIn_InputRq()
		self.Check_KeepUrls_in_outputUrl()
		self.Check_KeepCust_in_outputUrl()

#url='http://kayo-gam-proxy-perf/gampad/live/ads?path=Upath&ss_req=Uss_req&env=Uenv&gdfp_req=Ugdfp_req&unviewed_position_start=Uunviewed_position_start&impl=Uimpl&sz=Usz&vad_type=Uvad_type&iu=/21783347309/espn.au/kayo/Tdevice_type&pp=Upp&tfcd=Utfcd&output=xml_vast3&ad_rule=Uad_rule&cmsid=Ucmsid&vid=Uvid&ssss=Ussss&correlator=Ucorrelator&ppid=Uppid&url=Uurl&description_url=http://www.espn.com/video&scor=Uscor&mridx=Umridx&pod=Upod&npa=Unpa&is_lat=Uis_lat&rdid=Urdid&idtype=Uidtype&min_ad_duration=Umin_ad_duration&ip=Uip&vpos=Uvpos&pmnd=Upmnd&pmxd=Upmxd&pmad=Upmad&user_agent=Uuser_agent&msid=Umsid&an=Uan&cors=2023-03-14%2020:49:19.339297&cust_params=series%3DTseries%26sp%3DTsp%26chan%3DTchan%26vdm%3Dlive%26authp%3DTauthp%26plt%3DTplt%26vps%3DTvps%26adPod%3DTadPod%26ppid%3DTppid%26refDomain%3DTrefDomain%26distAssetId%3DTdistAssetId%26bundleId%3DTbundleId%26isDnt%3DTisDnt%26linearProvider%3Despn2%26metadata_sport%3DTmetadata_sport%26dph%3DTdph%26sportSeriesName%3Dmotor_Get_Up_%26metadata_live%3DTmetadata_live%26device_os%3DTdevice_os%26device_type%3DTdevice_type%26metadata_assetId%3DTmetadata_assetId%26metadata_contenttype%3DTmetadata_contenttype%26metadata_state%3DTmetadata_state%26metadata_suburb%3DTmetadata_suburb%26metadata_title%3DTmetadata_title%26metadata_woId%3D222222%26excl_cat%3Dgambling%2Codds%26TestCaseName%3DParam_Order_Test_1%26teamA%3DSRH%26teamB%3DBOS%26sportFixtureId%3Dmotor_6792%26TCID%3D1'
#st = KeepParamTest(url)
#st.Check_KeepUrls_in_outputUrl()#KeepTypeParamsIn_InputRq()

def __test():
	with open('Response.json', 'r') as f:
		data=json.load(f)
		hits=data['rawResponse']['hits']['hits']
		length=len(hits)

		for item in hits:
			url = item['_source']['url']
			st = KeepParamTest(url)
			st.TestKeepTypeParams()
		print(len(hits))
#__test()