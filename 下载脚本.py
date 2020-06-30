import json
import urllib.request,urllib.parse
import os
f = open('test_data.json',encoding='utf-8')
res = f.read()
data = json.loads(res)
print(len(data))
print(data)
cases = data[0]['cases']
print(cases)
for case in cases:
    print(case["case_id"],case["case_type"])
    filename = urllib.parse.unquote(os.path.basename(case["case_zip"]))#获取文件名
    print(filename)
    urllib.request.urlretrieve(case["case_zip",filename])#下载题目包到本地