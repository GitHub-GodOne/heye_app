import hashlib
import os
import re
import subprocess

import execjs
import requests
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponse, StreamingHttpResponse
from urllib3.exceptions import InsecureRequestWarning
import json
from myapp import settings
class requests_m3u8(APIView):
    def get(self, request):
        url = request.GET.get("url")
        def down_chunk_file_manager(urls):
            yield requests.get(urls).content
        response = StreamingHttpResponse(down_chunk_file_manager(url))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="index.ts"'
        return response
        # my_url = {'url': 'https://apd-vlive.apdcdn.tc.qq.com/vipzj.video.tc.qq.com/h0022ah1yrf.mp4?vkey=235F5F99FB7A9B5A76F7DD02EA43F8D39F1AA5811D6D24187CF9818107403EEEC117852D5B047B98047C86D6B6F131458CE7CED0790332B022E7AA22645F1C1479A58245813C02D4F348C8DF17BC62FB77EADFFF665C3D3D5B1A61828DA43D6890B105C33CF06168FCAF4ECB64FFF9235A35626E5ED6ECC5', 'player': 'dplayer', 'code': 200, 'success': 1, 'type': 'mp4', 'msg': '数据正常', 'title': '腾讯视频', 'tishi': '★手下留情，请勿盗用★'}
        # return redirect(my_url["url"])

class detail(APIView):
    def __init__(self):
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    def get(self, request):
        url = request.GET.get("url")
        urls = str(url).split("||--||")
        text = self.select(urls)
        # def down_chunk_file_manager(urls):
        #     yield self.select(urls)
        # response = StreamingHttpResponse(down_chunk_file_manager(urls))
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = f'attachment;filename="index.m3u8"'
        if text is None:
            return HttpResponse(json.dumps({"code": 1, "url":"没有数据源！！！"}, ensure_ascii=False))
        print(json.dumps(text, ensure_ascii=False))
        return HttpResponse(json.dumps(text, ensure_ascii=False))
        # return redirect(text)

    def select(self, urls):
        for url_test in urls:
            if ".m3u8" in url_test:
                # file_path = self.return_file_path(url_test)
                # if os.path.exists(file_path):
                #     with open(file_path, "r") as f:
                #         text = f.read()
                #     return text
                try:
                    req = requests.get(url_test)
                    if req.status_code != 200:
                        continue
                    # return {"code": 0, "type": "m3u8", "url": url_test}
                except:
                    print("出错")
                    continue
                # url_two = re.findall("(.*?/index\.m3u8)", req.text)
                # if len(url_two) == 0:
                #     return {"code":1, "type":"m3u8", "url": None}
                # url_list = url_test.split("/")
                # req_url = url_list[0] + "//" + url_list[2] + url_two[0]
                # try:
                #     req = requests.get(req_url, headers=self.head)
                #     if req.status_code != 200:
                #         continue
                # except:
                #     print("出错")
                #     continue
                # text = req.text
                # with open(file_path, "w") as f:
                #     f.write(text)
                return {"code": 0, "type": "m3u8", "url": url_test}
            if "y" == url_test[0] and "j" == url_test[1]:
                text = self.get_mp4_url(url_test)
                if text["play"] == "mp4":
                    print(text["url"])
                    return {"code": 0, "type": "mp4", "url": text["url"]}
                else:
                    print(text["play"])
            else:
                text = self.get_m3u8(url_test)
                if "视频数据丢失，请联系管理员修复!" == text:
                    print("视频数据丢失，请联系管理员修复!")
                    text = self.get_txt(url_test)
                    if "视频数据丢失，请联系管理员修复!" == text:
                        print("视频数据丢失，请联系管理员修复!")
                        continue
                    return text
                return text

    def return_file_path(self, main_url):
        md5_url = self.md5(main_url)
        file_path = os.path.join(settings.BASE_DIR, "src")
        file_path = os.path.join(file_path, "m3u8")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return os.path.join(file_path, f"{md5_url}")

    def get_m3u8(self, url):
        # file_path = self.return_file_path(url)
        # if os.path.exists(file_path):
        #     with open(file_path, "r") as f:
        #         text = f.read()
        #     os.remove(file_path)
        #     return text
        bash_path = os.path.join(settings.BASE_DIR, 'sign')
        m3u8_main_path = os.path.join(bash_path, 'js/m3u8_main.js')
        m3u8_template_path = os.path.join(bash_path, 'js/m3u8_template.js')
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "referer": "https://www.m3u8.tv.cdn.8old.cn/jx.php?url=https://www.iqiyi.com/v_19rra0h3wg.html"
        }
        # url = "https://www.iqiyi.com/v_19rra0h3wg.html"
        text = requests.get(f"https://www.m3u8.tv.cdn.8old.cn/m3u8tv/api.php?url={url}", headers=headers).text
        domain = re.findall(r"var domain = '(.*?)';", text)[0]
        host = domain
        referer = re.findall(r"'referer':'(.*?)'", text)[0]
        ref = "0"
        time = re.findall(r"var time = '(.*?)';", text)[0]
        ip = re.findall(r"'ip':'(.*?)'", text)[0]
        type = ''
        with open(m3u8_template_path, "r", encoding="utf8") as f:
            test = f.read()
        test = test.replace('var host = ""', f'var host = "{host}"').replace('var domain = ""',
                                                                             f'var domain = "{domain}"').replace(
            'var time = ""', f'var time = "{time}"').replace('var url = ""', f'var url = "{url}"')
        with open(m3u8_main_path, "w", encoding="utf8") as f:
            f.write(test)
        result = subprocess.Popen(["nodejs", m3u8_main_path], shell=False, stdout=subprocess.PIPE)
        other = result.stdout.readline().decode("utf-8").strip()
        token = result.stdout.readline().decode("utf-8").strip()
        keys = re.findall(r"'keys':'(.*?)'", text)[0]
        keep = result.stdout.readline().decode("utf-8").strip()
        key = re.findall(r"'key':'(.*?)','ios'", text)[0]
        data = {
            'url': url,
            'referer': referer,
            'ref': ref,
            'time': time,
            'ip': ip,
            'type': type,
            'other': other,
            'token': token,
            'keys': keys,
            'keep': keep,
            'key': key,
            'ios': ''
        }

        headers = {
            "content-length": '440',
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
            "accept": 'application/json, text/javascript, */*; q=0.01',
            "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
            "x-requested-with": 'XMLHttpRequest',
            "sec-ch-ua-mobile": '?0',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
            "sec-ch-ua-platform": '"Windows"',
            "origin": 'https://www.m3u8.tv.cdn.8old.cn',
            "sec-fetch-site": 'same-origin',
            "sec-fetch-mode": 'cors',
            "sec-fetch-dest": 'empty',
            "accept-encoding": 'gzip, deflate, br',
            "accept-language": '"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"',
        }
        # requests.get("https://rty.w2008.store/api.php")
        # requests.get("https://rty.w2008.store/api.php")
        try:
            my_url = requests.post("https://www.m3u8.tv.cdn.8old.cn/m3u8tv/%E3%80%80.php", headers=headers,
                                                data=data).json()
            if (my_url["type"] == "mp4" or my_url["type"] == "auto"):
                print(my_url)
                print(my_url["url"])
                return {"code": 0, "type": "mp4", "url": my_url["url"]}
            result = requests.get(my_url["url"]).text
        except:
            # with open(file_path, "w") as f:
            #     f.write("视频数据丢失，请联系管理员修复!")
            return "视频数据丢失，请联系管理员修复!"
        if len(re.findall("https://cdn.oss-cn", result)) != 0:
            # result = result.replace("https://cdn.oss-cn",
            #                         "/requests_m3u8?url=https://cdn.oss-cn")
            # with open(file_path, "w") as f:
            #     f.write(result)
            return {"code": 0, "type": "file_path_m3u8", "url": my_url["url"]}
        else:
            # result = result.replace("/key/token",
            #                         "/requests_m3u8?url=https://cdn.oss-cn-hangzhou-shanghai.myqcloud.com.zhegeyuming.top/key/token")
            # with open(file_path, "w") as f:
            #     f.write(result)
            return {"code": 0, "type": "m3u8", "url": my_url["url"]}

    def get_txt(self, main_url):
        file_path = self.return_file_path(main_url)
        if os.path.exists(file_path):
            os.remove(file_path)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        str123 = requests.get(url=f"https://jx.aidouer.net/?url={main_url}", proxies={"http": None, "https": None}).text
        str123 = re.findall("(var Time = \".*?Token1\);)", str123, re.S)[0]
        str123 = str123.replace("$.md5", "md51").replace("XXTEA.", "")
        bash_path = os.path.join(os.path.join(settings.BASE_DIR, 'sign'), 'js')
        fs = open(os.sep.join([bash_path, 'main.js']), encoding='utf8')
        text = fs.read()
        fs.close()
        ip_result = requests.get(url="https://pv.sohu.com/cityjson?ie=utf-8")
        text = text.replace("我是模板啦啦啦", str123).replace("ip地址替换位置", ip_result.text)
        cxt = execjs.compile(text)
        a = cxt.call("doit")
        url = a[0]
        headers = a[2]
        Data = a[1]
        cookies = a[3]
        cookie = a[4]
        print(url)
        print(headers)
        print(Data)
        print(cookies)
        text = requests.post(url=url, proxies={"http": None, "https": None}, data=Data, headers=headers,
                             cookies=cookies).json()
        print(text)
        if text['status'] is not 1:
            print("视频数据丢失，请联系管理员修复!")
            # with open(file_path, "w") as f:
            #     f.write("视频数据丢失，请联系管理员修复!")
            return "视频数据丢失，请联系管理员修复!"
        with open(os.sep.join([bash_path, 'doit1.js']), 'r', encoding="utf-8") as f:
            text1 = f.read()
        text1 = text1.replace("替换", json.dumps(text)).replace("不要", json.dumps(Data)).replace("要", text["data"])
        with open(os.sep.join([bash_path, 'doit2.js']), 'w', encoding="utf-8") as f:
            f.write(text1)
        cmd = f"node {os.sep.join([bash_path, 'doit2.js'])}"
        with os.popen(cmd) as nodejs2:
            temp = nodejs2.read().replace('\n', '')
        print(temp)
        s = requests.Session()
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'referer': 'https://jx.aidouer.net/?url=https://www.iqiyi.com/v_19rsnp37uk.html',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }
        if "mp4" in temp:
            return {"code": 0, "type": "mp4", "url": temp}
        text123 = s.get(url=temp, proxies={"http": None, "https": None}, headers=headers, cookies=cookies, verify=False,
                        allow_redirects=False)
        try:
            url = text123.headers["location"]
        except:
            print("视频数据丢失，请联系管理员修复!")
            return "视频数据丢失，请联系管理员修复!"
        text = s.get(url=url, proxies={"http": None, "https": None}, headers=headers, cookies=cookies, verify=False,
                     allow_redirects=False).text
        with open(file_path, "w") as f:
            f.write(text)
        return {"code": 0, "type": "text_m3u8", "url": file_path}

    def md5(self, text):
        m = hashlib.md5()
        b = text.encode(encoding='utf-8')
        m.update(b)
        return m.hexdigest()

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
        with open(test_path, "r", encoding="utf8") as f:
            get_text = f.read()
        get_text = get_text.replace('console.log(II1lli("a71f96bb85908c093b5bc00ca59f8207"));',
                            f"console.log(II1lli(\"{hdMd5}\"));")
        print(hdMd5)
        with open(temp_path, "w", encoding="utf8") as f:
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
