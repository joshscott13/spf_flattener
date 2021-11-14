import subprocess
import re


def TxtFormatter(rdata) -> str:
    txt_record_list = []
    spf_txt = ""
    for item in rdata:
        if item.startswith("\"v=spf1"):
            spf_txt += item + ' '
        elif item.startswith("include"):
            spf_txt += item + ' '
        elif item.startswith("ip4:"):
            spf_txt += item + ' '
        elif item.startswith("-all") or item.startswith("~all"):
            spf_txt += item
            txt_record_list.append(spf_txt)
        elif item.startswith("\""):
            txt_record_list.append(item)
        else:
            return "No matching format"
    return txt_record_list
    

def query(domainName):
    #results = []
    try:
        with subprocess.Popen(["dig", domainName, "TXT"], stdout=subprocess.PIPE) as proc:
            result = proc.stdout.read().decode()
            return result
    except:
        pass
    # results = [r for r in split_text]
    # return results
test_record = ["\"v=spf1", "include:cnn.com", "include:nope.com", "ip4:192.168.1.0/24", "-all\"", "\"f44nnugnd32222ll-333\"", "\"Token:", "\"Testdata\""]

#print(TxtFormatter(test_record))


print(p)
hostname = 'npr.org'
query = query(hostname)
match = p.findall(query)
for m in match:
    print(m)
