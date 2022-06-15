import os
import re
import subprocess

import requests
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView

from myapp import settings

class get_m3u8(APIView):
    def get(self, requests):
        file_path = requests.GET.get("url")
        def down_chunk_file_manager(file_path):
            yield self.dosome(file_path)
        response = StreamingHttpResponse(down_chunk_file_manager(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="index.m3u8"'
        return response

    def dosome(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                text = f.read()
            return text

class mp4_text(APIView):
    def get(self, request):
        url = request.GET.get("url")
        urls = str(url).split("||--||")
        for i in urls:
            # if "mp4" in i:
            #     try:
            #         req = requests.get(i, timeout=(1.111, 1.01))
            #         if req.status_code != 200:
            #             urls.remove(i)
            #             continue
            #         return redirect(i)
            #     except Exception:
            #         return redirect(i)
            if "y" == i[0] and "j" == i[1]:
                text = self.get_mp4_url(i)
                if text["play"] == "mp4":
                    print(text["url"])
                    return redirect(text["url"])
                else:
                    print(text["play"])
        return redirect('https://www.baidu.com/')

    def get_mp4_url(self, name):
        bash_path = os.path.join(settings.BASE_DIR, 'sign')
        test_path = os.path.join(bash_path, 'js/test.js')
        temp_path = os.path.join(bash_path, 'js/temp.js')
        print(bash_path)
        url = f"https://test89.quelingfei.com:4438/wap.php?url={name}"
        text = requests.get(url).text
        GaoDuan2019 = re.findall('"GaoDuan2019": "(.*?)"', text)[0]
        time = re.findall('"time":"(.*?)"', text)[0]
        url_222 = re.findall('"url_222": "(.*?)"', text)[0]
        hdMd5 = re.findall('eval\((.*?)\);player', text)[0]
        hdMd5 = re.findall("val\('(.*)'\);", eval(hdMd5))[0]
        get_text = ""
        with open(test_path, "r") as f:
            get_text = f.read()
        get_text = get_text.replace('console.log(II1lli("a71f96bb85908c093b5bc00ca59f8207"));',
                            f"console.log(II1lli(\"{hdMd5}\"));")
        print(hdMd5)
        with open(temp_path, "w") as f:
            f.write(get_text)
        result = subprocess.Popen(["nodejs", temp_path], shell=False, stdout=subprocess.PIPE)
        hdMd5 = result.stdout.readline().decode("utf-8").strip()
        print(hdMd5)
        header = {
            'Host': 'test89.quelingfei.com:4438',
            'Connection': 'keep-alive',
            'Content-Length': '194',
            'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://test89.quelingfei.com:4438',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://test89.quelingfei.com:4438/wap.php?url={name}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        data = {
            "time": time,
            "key": hdMd5,
            "GaoDuan2019": GaoDuan2019,
            "url": name,
            "url_222": url_222
        }
        text = requests.post("https://test89.quelingfei.com:4438/api.php", headers=header, data=data).json()
        return text