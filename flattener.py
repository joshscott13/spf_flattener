import subprocess
import re
from ipaddress import ip_network, ip_address


class TxtRecord:
    

    def __init__(self, domainName) -> str:
        self.domainName = domainName
        self.txtrecords = self._queryResults()


    def _queryResults(self) -> str: # returns the TXT records for the domain given
        p = re.compile('(\".*\")')
        txtrecordlist = []
        try:
            query = subprocess.run(["nslookup", "-type=TXT", self.domainName], capture_output=True, text=True)
            match = p.findall(query.stdout)
            txtrecordlist = [m for m in match]
            return txtrecordlist
        except:
            pass
        

class SPFRecord(TxtRecord):
    
    def __init__(self, domainName):
        super().__init__(domainName)
        self.spfrecord = self._getSPFRecord()
        # self.includedHosts = self._getIncludedHosts()
        # self.ip4List = self._getIP4Hosts()
        # self.includedHostIps = self._getIncludedHostIps()


    def _getSPFRecord(self):




    def _getIP4Hosts(self) -> list:
        ipHostList = []
        ipreg = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/*\d{0,2}')
        for record in self.txtrecords:
            if record.startswith("\"v=spf1"):
                split = record.split()
                for i in split:
                    match = ipreg.findall(i)
                    if match:
                        ipHostList.append("ip4:" + match[0])
        return ipHostList
    

    def _getIncludedHostIps(self):
        iplist = []
        ipreg = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/*\d{0,2}')
        for record in self.includedHosts:
            iplist.append(record)


    def hostLookup(self, host) -> str: #returns 'txtrecord', indicating recursion needed, or an ip address
        try:
            with subprocess.Popen(["nslookup", host], stdout=subprocess.PIPE) as proc:
                result = proc.stdout.read().decode()
                print(result)
                if "*** Can't find" in result:
                    return "need to check txt record"
                else:
                    return "test"
        except:
            pass


    def flatten(self):
        flattened = ""
        for host in self.includedHosts:
            pass


spf1 = SPFRecord('cnn.com')
print(spf1.txtrecords)