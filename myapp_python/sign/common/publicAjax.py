from django.http import JsonResponse

"""后端对前端的请求的回应
  status:0 表示成功，1表示失败
"""
def myJsonResponse(status, msg_value, dictData):
    dictionary = {
        "status": status,
        "msg": msg_value,
        "data": dictData
    }
    return JsonResponse(dictionary, json_dumps_params={'ensure_ascii':False})

def myJsonResponse2(code, msg_value,oaurl,data=None):
    dictionary = {
        'code': code,
        "msg": msg_value,
        "oaurl": oaurl,
        "data":data
    }
    return JsonResponse(dictionary, safe=False, json_dumps_params={'ensure_ascii': False})