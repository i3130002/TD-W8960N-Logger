import requests
import base64

class AdslStatus:
    # url = "https://webhook.site/daed3632-7829-4ec8-896d-66040e5451b1"
    url = "http://192.168.1.1/"
    deviceInfoUrl = "http://192.168.1.1/info.html"
    deviceStatistics = "http://192.168.1.1/statsadsl.html"

    def __init__(self,username="admin",password="admin",isDebug=True):
        self.username = username
        self.password = password
        self.isDebug = isDebug
        self.login()

    def login(self):
        cookies = {'Authorization': "Basic "+(base64.b64encode((self.username+":"+ self.password).encode("ascii"))).decode('utf-8')}
        r = requests.get(self.url,cookies=cookies)
        if not "Authorization" in r.cookies:
            raise Exception("Login Error!!! code:%s body:%s".format(r.status_code,r.text))
        self.cookies = {'Authorization': r.cookies["Authorization"]}
        self.debug(self.cookies)
    
    def writeToFile(self,responseTest):
        with open ("out.html", "w") as f:
            f.write(responseTest)
    
    def getPage(self,pageURL):
        r = requests.get(pageURL,cookies=self.cookies)
        # self.writeToFile(r.text)
        return (r)

    def extractDataDeviceInfo(self):
        responseText = (self.getPage(self.deviceInfoUrl)).text
        info = self.infoProcessor(responseText)
        info["System Running Time:"] = self.extractItemFromHTML(responseText,"System Running Time:")
        self.debug(info)

        responseText = (self.getPage(self.deviceStatistics)).text
        statics = self.staticsXDSLProcessor(responseText)
        self.debug(statics)
        return({**info, **statics})

    def extractItemFromHTML(self,htmlData,itemStr):
        itemIndex = htmlData.index(itemStr) + len(itemStr+ "</td> <td class=\"dataStyle\">")
        item = htmlData[itemIndex:htmlData.index("</td>",itemIndex)]
        self.debug(item)
        return item

    def infoProcessor(self,htmlData):
        startIndex = htmlData.index("var info = '")+ len("var info = '")
        endIndex = htmlData.index("|'.split('|');",startIndex)
        info = htmlData[startIndex:endIndex].split("|")
        #exp ATM WAN|atm0(1/66)|ppp0|PPPoE|Connected|100.64.1.122||172.30.0.18|3Day(s) 10:58:04|d4:6e:0e:b4:a6:99
        info = {"Internet Up Time:": info[8],"WAN IP Address:":info[5] }
        self.debug(info)
        return info

    def staticsXDSLProcessor(self,htmlData):
        snrDown,snrUp = self.staticExtractor(htmlData,"SNR Margin (0.1 dB):</td><td>","</td><td>","</td>")
        self.debug({"SNR Margin Down (0.1 dB):": snrDown,"SNR Margin Up (0.1 dB):":snrUp})
        rateDown , rateUp = self.staticExtractor(htmlData,"Attainable Rate (Kbps):</nobreak></td><td>","</td><td>","</td>")
        self.debug({"Attainable Rate Down (Kbps):": snrDown,"Attainable Rate Up (Kbps):":snrUp})
        return {"SNR Margin Down (0.1 dB):": snrDown,
                "SNR Margin Up (0.1 dB):":snrUp,
                "Rate Down":rateDown,
                "Rate Up":rateUp}


    def staticExtractor(self,htmlData,start,middle,end):
        item1start = htmlData.index(start) + len(start)
        item1End = htmlData.index(middle,item1start)
        item2start = item1End + len(middle)
        item2End = htmlData.index(end,item2start)
        item1 = htmlData[item1start:item1End]
        item2 = htmlData[item2start:item2End]
        return ([item1,item2])

    def debug(self,data):
        if self.isDebug:
            print (data)