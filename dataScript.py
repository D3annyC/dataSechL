# -*- coding: utf8 -*-
import json
import math
import requests
from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import codecs

sched= BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def main():
    result = requests.get("http://218.161.81.10/app/sub4.asp?T1=VAN01")
    result.encoding='utf-8'
    root = etree.fromstring(result.content, etree.HTMLParser())
    jsonData = "["

    #split string from caption
    venRowData = root.xpath("//section/table[@class='table1']/caption/text()")
    ven =venRowData[0]
    ven =ven.split('(')
    time =ven[1].split(')')

    # add ven and time
    venInfo ='{"ven":"'+ven[0]+'","time":"'+time[0]+'",'
    jsonData +=venInfo

    for row in root.xpath("//section/table[@class='table1']/tbody/tr[position()>1]"):
        column = row.xpath("./td/text()")
        tmp= '"%s":"%s",' % (column[0], column[1])
        jsonData += tmp

    # delete last ','
    print(datetime.datetime.now())
    print(jsonData[0:-1] + '}]')

if __name__ == "__main__":
    main()

sched.start()
