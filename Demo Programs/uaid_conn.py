import mail
import utils,csv,os,sys
import time
from operator import itemgetter
from datetime import datetime,timedelta
#current time
now=datetime.now()
before=now-timedelta(hours=12)
#current time in epoch format
to = utils.get_date(date=now)
#last one hour time in epoch format
frm = utils.get_date(date=now, th=12)
#get query for reconnected
device=['Device_IPv4','Device_IPv6']
avg=[]
node_avg=[]
node_based_avg={}
files=[]
for ip in device:
    query = utils.get_query(frm=frm,to=to, ip=ip)
    #Get data from elasticsearch
    result = utils.get_details(index="prod_push_cep-*", body=query)
    #fetch details and store it in list
    result = utils.fetch_hits(result=result, ip=ip)
    
    data=utils.sort_data(result)
#    x=utils.sort_node_based(data)
    #print x
    filename='/var/www/html/Report/'+ ip + '_'+datetime.now().strftime("%Y%m%d-%H%M")+'.csv'
    header1=["UAID","IP","Host"]
    temp=1
    for v in data.itervalues():
        if len(v) > temp:
             temp=len(v)
    
    for i in range(temp):
        header1.extend(["Diff"])
    utils.convert_csv(data=data, header=header1,filename=filename)
     
    utils.sort_csv(filename=filename)
    
#    avg.append(utils.calculate_avg(filename=filename))
    avg.extend( utils.calculate_avg(filename=filename))
    node_avg.append(utils.calculate_node_avg(filename=filename))
    utils.plot_graph(filename=filename,ip=ip)
#    files.append(filename)
    print(files)


#print len(avg)
#print node_avg
filename=utils.sort_node_based(node_avg)
header=["Node","IPv4 Time","IPv4 UAID Count","IPv6 Time","IPv6 UAID Count"]
files.extend([filename,'/mnt/push_test/Device_IPv4.png','/mnt/push_test/Device_IPv6.png','/mnt/push_test/diff_Device_IPv4.csv','/mnt/push_test/diff_Device_IPv6.csv'])
print("############################################")
print(files)

f= open("/mnt/push_test/message.txt","w+")
f.write("Hi, \n\nAverage connected time for IPv4 devices: " + str(round(avg[0],2))+" minutes" +"\n\n" + "Total IPv4 Devices: " + str(avg[1]) +"\n\n" + "Average Connected time for IPv6 devices: "+ str(round(avg[2],2))+" minutes"+"\n\n" +"Total IPv6 Devices: "+str(avg[3])+"\n\nTime Duration: "+str(before)+" to "+str(now)+"\n\nDownload report from below URL:\n\n"+"http://10.144.182.51/Report/"+"\n\nRegards, \nElastic Stack")
#
f.close()

mail.sendmailCSV(files)
