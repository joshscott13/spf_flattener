import subprocess
import re
from ipaddress import ip_network, ip_address

def validateIPaddress(ip):
    try:
        if ip_address(ip):
            print(f"{ip} is valid!")
    except ValueError as e:
        print(f"{ip} is NOT a valid IPv4 address!")


def validateIPsubnet(ipsubnet):
    try:
        if ip_network(ipsubnet, strict=False):
            print(f"{ipsubnet} is valid")
    except ValueError as e:
        print(f"{ipsubnet} is NOT a valid IPv4 network!")

class TxtRecord:
    

    def __init__(self, domainName) -> str:
        self.domainName = domainName
        self.txtrecords = self._queryResults()


    def _queryResults(self) -> str: # returns the TXT records for the domain given
        p = re.compile('(\".*\")')
        txtrecordlist = []
        try:
            with subprocess.Popen(["dig", self.domainName, "TXT"], stdout=subprocess.PIPE) as proc:
                result = proc.stdout.read().decode()
                txts = p.findall(result) # regex searches through the result of the query for strings starting and ending in "
                for m in txts:
                    txtrecordlist.append(m)
                return txtrecordlist
        except:
            pass
        

class SPFRecord(TxtRecord):

    def __init__(self, domainName):
        super().__init__(domainName)
        self.includeHosts = self._getIncludedHosts()
    #     self.ipList = []

    def _getIncludedHosts(self) -> list: # parses the "include:" directives out of the SPF string
        hostList = []
        for record in self.txtrecords:
            if record.startswith("\"v=spf1"):
                split = record.split()
                for i in split:
                    if i.startswith("include:"):
                        hostList.append(i.replace("include:", ""))
        return hostList


spf1 = SPFRecord('cefcu.com')
for host in spf1.includeHosts:
    print(host)
for txtrecord in spf1.txtrecords:
    print(txtrecord)