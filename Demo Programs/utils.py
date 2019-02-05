from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from collections import defaultdict
import seaborn as sns
#import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
import json, csv, operator
from datetime import datetime,timedelta
import pandas as pd
import time
def get_date(date,td=0,th=0,tm=0):
    date = date-timedelta(hours = th, minutes=tm)
    # date= date.total_seconds()
    date=int(date.strftime("%s")) * 1000
    return date
def get_object():
    es=Elasticsearch(['http://10.135.129.104:9200'])
    return es
def get_details(index, body):
    es = get_object()
    return es.search(index=index,scroll="2m",size=10000,body=body)

def get_query(frm, to, ip):
    query = {
    "sort": [
        {
          "@timestamp": {
            "order": "desc",
            "unmapped_type": "boolean"
          }
        }
      ],
      "_source": {
       "includes": ["UAID","Log_Msg","@timestamp","original_timestamp",ip,"host"]
      },
      "query": {
        "bool": {
          "must": [
            {
              "bool": {
                "should": [
                 # {
                 #   "match_phrase": {
                 #     "host.keyword": "prod-jmn-push-cep-p301"
                 #   }
                 # },
                 # {
                 #   "match_phrase": {
                 #      "host.keyword": "prod-jmn-push-cep-p302"
                 #   }
                 # },

                  {
                    "match_phrase": {
                      "Log_Msg.keyword": "Hello - Reconnected"
                    }
                  },
                  {
                    "match_phrase": {
                      "Log_Msg.keyword": "\"Device disconnected"
                    }
                  },
                  {
                    "match_phrase": {
                      "Log_Msg.keyword": "Hello - Connected"
                    }
                  }
                ],
                "minimum_should_match": 1
              }
            },
          {
          "exists": {
            "field": ip
             }
           },
            {
              "range": {
                "@timestamp": {
                  "gte": frm,
                  "lte": to,
                  "format": "epoch_millis"
                }
              }
            }
          ]
        }
      }
    }
    return json.dumps(query)

def fetch_hits(result,ip):
    es = get_object()
    data = []
    sid = result['_scroll_id']
    scroll_size = result['hits']['total']
    # Start scrolling
    while (scroll_size > 0):
        #print "Scrolling..."
        page = es.scroll(scroll_id = sid, scroll = '2m')
        # Update the scroll ID
        sid = result['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        hits=page['hits']['hits']
        #print "scroll size: " + str(scroll_size)
        # Do something with the obtained page
        for i in hits:
           epoch_time = i['sort'][0]
           UAID = i['_source']['UAID']
           log_msg= i['_source']['Log_Msg']
           p={"sort": epoch_time, "UAID": UAID, "log_msg": log_msg, "IP": i['_source'][ip], "original_timestamp": i['_source']['original_timestamp'] , "host" : i['_source']['host']}
           data.append(p)
#           print p

    return data

def sort_data(result):
    my_data = {}
    for i in result:
       a = i['sort']
       connect =[]
       discon = []
       if my_data.has_key(i['UAID']):
          connect = my_data[i['UAID']][2]
          discon = my_data[i['UAID']][3]
    
       if i["log_msg"]=="Hello - Connected" or i["log_msg"] == "Hello - Reconnected":
            connect.append(a)
    
       else:
            discon.append(a)
    
       my_data[i['UAID']] = [i["IP"],i["host"],connect, discon]
    my_data2 = {}
    node_based = {} 
    for k,v in my_data.iteritems():
        fmt= '%Y-%m-%d %H:%M:%S'
        ip=v[0]
        host=v[1]
        connect=v[2]
        discon=v[3]
        i=0;j=0;d=[]
        while(len(connect)>0 and len(discon) >0 and i<len(connect) and j<len(discon)):
            if connect[i] < discon[j]:
                c = datetime.strptime(time.strftime(fmt, time.localtime(connect[i]/1000)),fmt)
                d = datetime.strptime(time.strftime(fmt, time.localtime(discon[j]/1000)),fmt)
                #df = round(float((d-c).seconds) /60 , 2)
                df = round(float((d-c).seconds) /60 , 2)
                i+=1;j+=1
                if my_data2.has_key(k):
                   my_data2[k].append(df)
                else:
                   my_data2[k] = [ip,host]
                   my_data2[k].append(df)
    #            print(my_data2)
            elif connect[i] > discon[j]:
                j+=1
            else:
                i+=1; j+=1
         
#    print my_data2
    return my_data2


def sort_csv(filename):
    reader = None
    data=[]
    with open(filename,'rb') as f:
         reader = csv.reader(f)
         data= list(reader)
    header=data[0]
    del data[0]
    st = sorted(data, key=lambda x:float(x[3]), reverse=True)
    w = csv.writer(open(filename,'w'))
    w.writerow(header)
    for i in st:
        w.writerow(i)

def convert_csv(data,header,filename):
    with open(filename,'w') as f:
         w = csv.writer(f)
         w.writerow(header)
         for k,v in data.items():
            l = []
            l.append(k)
            s = ",".join(map(str,v))
            s = s.split(",")
            l.extend(s)
            #print l
            w.writerow(l)
         f.close()
def calculate_avg(filename):
     df = pd.read_csv(filename)
     diff = df["Diff"]
     len(diff)
     avg=[diff.mean(),len(diff)]
     return avg

def calculate_node_avg(filename):
     df = pd.read_csv(filename)
     diff = df["Diff"]
     p = df.groupby(['Host']).mean()
     c = df.groupby(['Host']).count()
     c = c["UAID"].to_dict()
     l =p["Diff"].round(2).to_dict()
     d = defaultdict(list)
     for a,b in l.items() + c.items():
         d[a].append(b)
     len(diff)
    # avg=[d]
     return d

#################graph plotted######################


def plot_graph(filename,ip):
     df = pd.read_csv(filename,sep=',')
     bins = [0.1,0.2,0.3,0.5,1,2,3,4,5,6,7,8,9,10,100,500,1000,1500]
     category=pd.cut(df.Diff,bins)
     category=category.to_frame()
     category.columns=['range']
     df_new=pd.concat([df,category],axis=1)
#print df_new
     plt.figure(figsize=(18,12))
     plt.title("UAID Time Analysis")

     ax=sns.countplot(x='range',data=df_new,palette='hls')
     ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
     plt.tight_layout()
     #plt.show()

#df = data.ix[-5:,['Range','Count']]
#ax=sns.countplot(x='range',data=df_new,figsize=(18,12))
#plt.title("UAID Time Analysis")
     #plt.show()
     fig=ax.get_figure()
     if ip=='Device_IPv4':
        fig.savefig('Device_IPv4.png')
     if ip=='Device_IPv6':
        fig.savefig('Device_IPv6.png')
     s=df.groupby(pd.cut(df['Diff'],bins=bins)).size()
     print(s)
     filename1 = '/mnt/push_test/diff_'+ip+'.csv'
     
     #print data5
     data= dict(s)
     #for key in sorted(data.iterkeys()):
         #    print "%s: %s" % (key, data[key])
      #       data4={key:data[key]}
      #       print data4
     #data = sorted(data.iterkeys())
     #print data
     header=["Range","Count"]
     #print data
     f = open(filename1,'w')
     w = csv.writer(f)
     w.writerow(header)
     for i in data.iteritems():
         w.writerow(i)
     f.close()
    
     
     ##################read file for counting percentile##########
     data2=[]
     with open(filename1,'rb') as f:
          c = csv.reader(f)
          data2=list(c)
     del data2[0]
     df = pd.read_csv(filename1,sep=',')
     c=df["Count"]
#     print data2
#     print(type(data2))
     count=df["Count"].sum()
     p=[]
     for i in c:
         agg = float((i/count)*100)
         p.append(agg)
#     print p
     d=len(data2)
     for i in range(0,d):
         data2[i].append(p[i])
#         print data2[i]
     ##################dump data ##########333
     with open(filename1,'w') as f:
          c = csv.writer(f)
          header.append("Percentile")
          c.writerow(header)
          for i in data2:
              c.writerow(i)
     
     #data = pd.read_csv(filename1,sep=',')
     #df = data.ix[-5:,['Range','Count']]
     #ax=df.plot(x='Range', y='Count', kind='bar',figsize=(18,12))
     #plt.title("UAID Time Analysis")
     #plt.show()
     #fig=ax.get_figure()
     #fig.savefig('diff_'+ip+'.png')

def sort_node_based(node_avg):
     d = defaultdict(list)
     for a,b in node_avg[0].items():
         d[a].append(b)
     for a,b in node_avg[1].items():
        if d.has_key(a):
            d[a].append(b)
        else:
            d[a]=[['-','-'],b]
     for a,b in d.items():
        if len(b) < 2:
            d[a].append(['-','-'])
     filename='/var/www/html/Report/node_analysis_'+datetime.now().strftime("%Y%m%d-%H%M") +'.csv'
     with open(filename,'w') as f:
          header=['Node','IPv4 avg in minutes','IPv4 Devices count','IPv6 avg in minutes','IPv6 Devices count']
          c =csv.writer(f)
          c.writerow(header)
          for k,v in d.items():
              l=[]
              l.append(k)
              for i in v: l.extend(i)
              print(l)
              c.writerow(l)
     return filename
