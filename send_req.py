import requests as rq
from datetime import datetime, timedelta
#from RandomUrlGen import RandomUrlGen
from RandomUrlGen import RandomOrderGen
from RandomUrlGen import RandomNumberOfParams
import random 
from Report import Report
import csv
import os
#from CsvHandler import CsvHandler


cors="cors="+str(datetime.now())
cors=cors.replace(' ','')

print(cors)
flag=0
while flag!=1:
	flag=int(input("please press 1 to continue.."))

TestCaseName=""
WOID=""
TESTCASE_FILE=os.getcwd()+"/TestCases/TestCases.csv"

cluster1="platform01"
cluster2="platform02"
##### STAGING HOSTS
hosts=["https://kayo-gam-proxy.content."+cluster1+".streamotion-platform-nonprod.com.au/gampad/live/ads?", "https://kayo-gam-proxy.content."+cluster2+".streamotion-platform-nonprod.com.au/gampad/live/ads?"]

##### PRODUCTION HOSTS
#hosts=["https://kayo-gam-proxy.content."+cluster1+".streamotion-platform-prod.com.au/gampad/live/ads?", "https://kayo-gam-proxy.content."+cluster2+".streamotion-platform-prod.com.au/gampad/live/ads?"]

#hosts=["https://kayo-gam-proxy-for-perf.content."+cluster1+".streamotion-platform-nonprod.com.au/gampad/live/ads?", "https://kayo-gam-proxy-for-perf.content."+cluster2+".streamotion-platform-nonprod.com.au/gampad/live/ads?"]
#first=1
#host="https://kayo-gam-proxy.content."+cluster2+".streamotion-platform-nonprod.com.au/gampad/live/ads?"

## HOST for PRODUCTION
host=hosts[random.randint(0,1)]
ESPN=['espn1', 'ESPN1', 'ESPN2', 'espn2']

input_data=[]
input_header=["TCID", "TC Name", "Encoded Input Request", "WoID", "Sport", "CompetitionText", "Expected_Url_Params", "Expected_Cust_Params"]
input_data.append(input_header)

TestCaseType_ParamOrderTest="AutoGenerated_ParamOrderTC"

def FormCustParam(cust_list:list):
	cust_param=""
	index=0
	#TCID="TCID%3D"+str(Request_count+1)
	#cust_list.append(TCID)
	for item in cust_list:
		if str(item)=='linearProvider':
			ind=random.randint(0,len(ESPN)-1)
			s=item+"%3D"+ESPN[ind]
		elif str(item)=='metadata_woId':
			s=item+"%3D"+WOID
		elif 'TCID' in item:
			s=item.strip()
		elif 'TestCaseName' in item:
			s=item.strip()
		else:
			s=item+"%3DRand"

		cust_param+=s
		index+=1
		if index<len(cust_list):
			cust_param+="%26"
	return cust_param

def FormRequest(url_list:list, cust_list:list):
	hostID = random.randint(0,1)
	req_url=hosts[hostID]
	index=0
	for item in url_list:
		if item=='cust_params':
			s=item+"="+FormCustParam(cust_list)
		elif 'cors=' in item:
			s=item
		else:
			s=item+"=Rand"
		req_url+=s
		index+=1
		if index<len(url_list):
			req_url+="&"
	return req_url


def CheckRequestStatus(resp):
	status_code = resp.status_code
	if str(status_code)!='200':
		print(status_code)
		return 0
	return 1

def StoreRequest(Rq_No, TestCaseName:str, url, args:list):
	row=[]
	row.append(str(Rq_No))
	row.append(TestCaseName+" "+str(Rq_No))
	row.append(url)

	for item in args:
		row.append(item)
	input_data.append(row)


def StoreInFile():
	rp = Report(input_data)
	rp.generateInputRequestFile()


last_date = datetime.now() - timedelta(days=6)
order_test_count = int(input("Please enter how many param order test you want to run(including all params in the input request)\n"))
order_test_count_2 = int(input("Please enter how many param order test you want to run(selecting random number of params in the input request)\n"))
WOID=str(input(f"Please enter a valid woID (Sport event date should not be older than {last_date})\n"))
Valid_sport_name = str(input(f"Please enter the sport name for {WOID} that is updated in staging server\n"))
competition_text = str(input(f"Please enter the competition text for {WOID} that is updated in staging server\n"))
run_userDefinedTcs = str(input("Would you like to run User Defined Testcases?Yes/No\n"))

START_TIME = datetime.now()

arg_list=[]
arg_list.append(WOID)
arg_list.append(Valid_sport_name)
arg_list.append(competition_text)

Request_count=1

for i in range(0,order_test_count):

	rnd = RandomOrderGen(cors, Request_count, TestCaseType_ParamOrderTest)
	
	url_arr = rnd.GetRandomOrderUrlParams()
	cust_arr = rnd.GetRandomOrderCustParams()

	url = FormRequest(url_arr, cust_arr)
	print(url)
	resp = rq.get(url)
	CheckRequestStatus(resp)
	StoreRequest(Request_count, TestCaseType_ParamOrderTest, url, arg_list)
	Request_count += 1


for i in range(0,order_test_count_2):

	rnd2 = RandomNumberOfParams(cors, Request_count, TestCaseType_ParamOrderTest)
	
	u_arr = rnd2.GetUrlParams()
	c_arr = rnd2.GetCustParams()

	url = FormRequest(u_arr, c_arr)
	resp = rq.get(url)
	CheckRequestStatus(resp)
	StoreRequest(Request_count, TestCaseType_ParamOrderTest, url, arg_list)
	Request_count += 1


def UpdateArgList(arg:list, custParmaList:list):
	woid = ""
	for item in custParmaList:
		if 'metadata_woId' in item:
			woid = item.split("%3D")[1]
			break
	if woid==arg[0]:
		return arg
	arr=[]
	arr.append(woid)
	arr.append("")
	arr.append("")
	return arr

def ExecTestCases(Request_count):
	f = open(TESTCASE_FILE, 'r')
	arr = csv.reader(f)
	row_count = 0
	rq_count = Request_count
	for row in arr:
		if row_count==0:
			row_count+=1
			continue
		testcasename = row[0].strip()
		url_params_arr = []
		if row[1]!="":
			url_params_arr = row[1].split(' ')
		url_params_arr.append(cors)

		cust_params_arr=[]
		if row[2]!="":
			cust_params_arr = row[2].split(' ')
		cust_params_arr.append("TCID%3D"+str(rq_count))
		cust_params_arr.append("TestCaseName%3D"+testcasename+"-"+str(rq_count))

		url_param_part=""
		cust_param_part="cust_params="

		for param in url_params_arr:
			url_param_part+=param.strip()
			if param!=url_params_arr[-1]:
				url_param_part+='&'

		for param in cust_params_arr:
			cust_param_part+=param.strip()
			if param!=cust_params_arr[-1]:
				cust_param_part+='%26'
		hostID = random.randint(0,1)
		if url_param_part=="":
			url = hosts[hostID]+cust_param_part
		else:
			url = hosts[hostID]+url_param_part+"&"+cust_param_part
		resp = rq.get(url)
		new_arg_list = UpdateArgList(arg_list, cust_params_arr)
		new_arg_list.append(str(row[3]))
		new_arg_list.append(str(row[4]))
		#print(new_arg_list)
		StoreRequest(rq_count, testcasename, url, new_arg_list)
		rq_count += 1
		#print(resp.status_code)
	return rq_count
		#print(f"url params:\n{url_params_arr}\ncust params:\n{cust_params_arr}\n")

if run_userDefinedTcs.lower()=='yes':
	Request_count=ExecTestCases(Request_count)

StoreInFile()

print("Executed request count = "+str(Request_count-1))
print("kibana search string: \n"+cors)
END_TIME=datetime.now()
time_required = END_TIME-START_TIME

print(f"Start time: {START_TIME.hour}:{START_TIME.minute}:{START_TIME.second}\nEnd time: {END_TIME.hour}:{END_TIME.minute}:{END_TIME.second}")
	#print(url)
	#print("\n")
