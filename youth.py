#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串，自动提现需要自己抓包
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可
#cookies1 = {
#  'YOUTH_HEADER': {"Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2252049058%22%2C%22%24device_id%22%3A%221764652f0e02f-059827c77e2824-734c1551-304704-1764652f0e1787%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221764652f0e02f-059827c77e2824-734c1551-304704-1764652f0e1787%22%7D; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1607497609,1607498515,1607509822,1607509848; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1607497678,1607509840","Accept":"*/*","Accept-Encoding":"br, gzip, deflate","Referer":"https://kd.youth.cn/html/taskCenter/index.html?uuid=63a44575e1a609a993f3a45d969463a3&sign=1bbb953227f309c1728cfd9aec64ceaa&channel_code=80000000&uid=52049058&channel=80000000&access=WIfI&app_version=1.8.0&device_platform=iphone&cookie_id=4fbc6df71ef5a4419007d522e7978b67&openudid=63a44575e1a609a993f3a45d969463a3&device_type=1&device_brand=iphone&sm_device_id=202012091505488954d08752814dc76ad09d5d960a125e0138d58c38909dc6&device_id=48833035&version_code=180&os_version=12.2&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66bpWKyt3Vqhnyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLCnl2mGjJiXr8-uapqGcXY&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66bpWKyt3Vqhnyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLCnl2mGjJiXr8-uapqGcXY&cookie_id=4fbc6df71ef5a4419007d522e7978b67","Connection":"keep-alive","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Content-Length":"0","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
#  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_nHSVk1s5Pk1lOQlYKzDUPU9y0FiOH2nIRqKp1NEljKT7rNHR8sm-zNM1uYF037ZLhJ3Xl0xswFUmY-cQ_hr0wixkQsFjVI3HBBKV9Vi7Arv9ucr9IYetIj9Zqs0mPLwQax27ryeUONkX-X3wt0uoM_8p9aCCWnT7B6DxIq_aMu1lIWm3-nbTMZwvIy9WHTVQAxhRcXP3wQsUVL_fiFGav0GTztg5LUsxA3vXsguFVktveW9i_myL2o4VfXQetIZKPEpAi5MUQcwait1gR_-tERUucxWg7c3GE1F8xf3taMDezfHHJU5M5T4cmDKKLQUSDFk6vZUFv9jWsEMbQYATXSh9XVVuHyjbMUP98uAwlV8yn-PgEeKj2QXQENu38MbV1D9hC_Zldwgh07Fel-CgRxqUICq204XjqAe8CyLgMzY7OhcbwC36mzYbKBsvX3mW279AcEkeTwZq9aVPLieAAHgxlkQBohGxPTrTtrFl8V14bGmXpP0NAsVMZzQjnnEfhJ_rVzEqP3RFa1iuolE2ZYDOkfYUkaXizU2--tS9fh8mk1zqWJnfMnqe7w1tUtaTvF01KoOQiVTfks1fHr6acOnBRxqvq4aZenVRBOjr3d2ekhjXpT-3SjVUpOl-OPM2J3VS15ww19NmkBUhhwXMDu1oxdtSKMqZ97W0EU-mc7CCHa2gXhzYTSIrEgSoRTuUFDWBfDIIcdwA0mvNRwjGfd2KPWqkXUAd7R5j7r3RRyR3424MpXjXe04GfgAToMX9EYwaQOq6XA2XyF7wxww9FDfknuqwRl1n38iadal8Y_o6OhAXR_Xa7A%3D%3D',
#  'YOUTH_REDBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o2kNNfxbTBdHNeGGUACeILyWR3zMN6Iw3IXfZs4Lu-yb9ynQmQje6lCx_IwxRVvI2SNym5MJ3oH5lFqmbtpdkJfwhB1sUJEdEgJ5iEwGnEtnWJDQPgSUh_43T95feCdA6znUBf7UdpUN7xhamwsNNLhpJQhUBfhwDALTbVR4ZFoUqbmU5_oFpLpMaZvPna0yapmK2CHq01Gm8906M2a8Yyz8581B6VKxfUCjOXTp60Ni_USELmZLu_uro5LasexBGbFs2UcKVJ8kcikr5O1JKn9Ll3vt0X_Js2iOmKNpGxk6rGkfQ73ASMbg5C3cfyC-Nz0qoZh5IA114JppKO1Gexo7-j_DzysNVWFEZEaBK3kuVRiBYLmguTdSjLnBYXI9QYKjGQoWaIC_qP2DB1GG3SEFuXw8HILC5p2mYIHdxs2VLrDy95yih4YYs5W2d2gG8KEqY7Oa4p82N9xgoJnvCo6UGEYElyq2YAkZdPcPQ_Dyl6-CpeIhPASLb5-pGLpvMyyD4zEEiKVb3Kd4wMWE6-NU3mfh6FMteGUbnudRfs2hoVwBdI5jfrPDVxTPMuupWN_v66XrUEZ8X2vXafYSw2uePpTnDMHPBgFGu3nNxcgvum1kSSJ47v0NxkwT20es2XTgQ7Rtl-jDzHTD8GO-2TmlTCbFaAs5Zs6Q0UVw7j55D4eMjYSeB7V-UkCjwQjT3CYYS2WExA7EciqEcEnNz4bEqwbT8go7CWQ8uwjQIB0BzICIRu65QR4Q9-ceoXnD9iXvfjl4MaGbkdWzby57YtA%3D%3D',
#  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_nHSVk1s5Pk1lOQlYKzDUPU9y0FiOH2nIRqKp1NEljKT7rNHR8sm-zNM1uYF037ZLhJ3Xl0xswFUmY-cQ_hr0wixkQsFjVI3HBBKV9Vi7Arv9ucr9IYetIj9Zqs0mPLwQax27ryeUONkX-X3wt0uoM_8p9aCCWnT7B6DxIq_aMu1lIWm3-nbTMZwvIy9WHTVQAxhRcXP3wQsUVL_fiFGav0GTztg5LUsxA3vXsguFVksbnVntwklOnWEj35P9JKZtF4b2oOYCUYYI1DCBgEP45QrBgmS7oXLwlTIXAQLrt9YCwgW1D539CSKRUfsi7GpzHiHr5-WvXO2S06LFzRIY4gvLMwIO_NYthNxhL__1gJ96ZMhwq6Cz5Z0PhLhouuJD2Dr6EjmI_vt03p7WLXf_bdsHi8TuDgZcDZDw9BOT8zlJNXlttqjGrpjIPgGIgTbPeDaPsjhuhZloWMiWIkT8uB_VACZA5fbmo5TN8vlxNndDqCDBOj4Wum7jM95ZfKiOU5ADjBRcjtsAF2yQW7cRqC__FrCBsmRLyWkQm25PmPaQ7c7vX71ctZNlWJ0anAaxP403iA-4wc1cbL4cMUjDQVktUhN82iNtvSmsEA1K0HmF4lrViZc7H1Dv4inYRyj_sU9XwxgicOr7Fx-fqAMgKJTiTElrbXcshCiTWVOGnlGY5qUkuytfODcOru26d603h9153iXtJ7owVh2LcmwYPwcnk1MVrKFIfxI7rlkiehf-Z8LwFo0iLSx-uY8HRHLEXdBZ4FrcPuOfBioitxAoR2JBAFVPheS5wHEXSmj1qEQ%3D',
#  'YOUTH_WITHDRAWBODY': ''
# }
cookies1 = {  
   'YOUTH_HEADER': {"X-Requested-With":"XMLHttpRequest","Connection":"keep-alive","Accept-Encoding":"gzip, deflate, br","Content-Type":"application/x-www-form-urlencoded","Origin":"https://kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2252049058%22%2C%22%24device_id%22%3A%22176ebc4e20f793-07a953abdd3f65-754c1551-304704-176ebc4e2101b7%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22176ebc4e20f793-07a953abdd3f65-754c1551-304704-176ebc4e2101b7%22%7D; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1612016284,1612017059,1612056599,1612056638; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1612017462,1612017488,1612017728,1612056634","Host":"kd.youth.cn","Referer":"https://kd.youth.cn/html/taskCenter/index.html?uuid=63a44575e1a609a993f3a45d969463a3&sign=f8c024433aa31b6ce5d285da42523cf3&channel_code=80000000&uid=52049058&channel=80000000&access=WIfI&app_version=1.8.2&device_platform=iphone&cookie_id=52d293208fa4afd11f680a641cb692c9&openudid=63a44575e1a609a993f3a45d969463a3&device_type=1&device_brand=iphone&sm_device_id=202012091505488954d08752814dc76ad09d5d960a125e0138d58c38909dc6&device_id=48833035&version_code=182&os_version=14.2&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwzXVphox2l7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonabr8-yZ4N5jbCEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwzXVphox2l7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonabr8-yZ4N5jbCEY2Ft&cookie_id=52d293208fa4afd11f680a641cb692c9","Accept-Language":"zh-cn","Accept":"*/*","Content-Length":"307"},
   'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ld4qx0YVkhCGk95BHaDHeU0mv6uDOh2O2ipjZo6NoleOFP3uDtc3FQBSvTz00HRezP6M12PoS3qF-BqoAYx72wrrh28EnIkoBp3K3HFMp8mGIU-nrSkrPPyPbKpQkemAHzLlKKlkAaBWqC4RjH3j6kZtSfkhgkCbUbXcfrn7oIQ7IQBBYaZdf_rs9sHVL5u5tHCXqnIteXU7_9ELcnO6p6aWuQbujag6qtaK8usbCFqOzuNM4nBHXnbrMgga0Fb3-5UopfUXHbtP_MqFpHO2RO6yHBhmvpBWjWODNcXKyByJWWSKSE93skNCWSdbxkywtbre2j3dQ5ZPgoYpVKtxAFvxydkBZ3Bbkt6Wc9QNjnAIaxFhyy-co70cjcK1Czjt0d5Q8sa9lou2FyRgLborAG7OEgwLpneTvyPlGKjc6ffYLEN3rYPa0HQNzHcbbbCqCxqj5gjlGHikMm_o5QbDq9_R-rA_nS9d-wWoIbzXN06WeeeaaYnKBtLC6lMRJ2SUPAQ7QxIXVHIIA9ynMMGFfaMhzjTJhWLPtbJ8TkbB2RMF4NtYh4gOpwH1vbdPcZ40ZqXtWhCDiTLzN8BwC6N1u1_S5aG8ea1eyRDIiz6T-XCURV-z0V5BqgS5e-MoF8GwjnnKp0kXzo5xD6pn2enhX3GKjJlvZht7Hc49z42-leeCKa7F9keieNgsfWCOBR5Iy8GQvyiRn6UYN8Um_HVfY4hzPZqkofe7SqvZNSVZMMtU-EmwdZmneILfITjzJFUmdXVaBMpHEmbXC6VcLX4SwCByxEECZHGYTsfoTdxNxKEm17Si2M6_aSQeRaez0jmqmAQVw5rVJg3w%3D%3D',
   'YOUTH_REDBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ka-LJ9wnbNzBhA0cz3iHWgEqXEh3bkBC0KSg93aV2LC-S2kpFYl_sQ9Ng1y2zq_SRMZ0l7L8Arl0rmgcn6uCMObkjGBykqoUNnvrLczNZAxsPvldu8lOTH6eBj7eYrYWk7odF79_wWrcR4Bkzgp_MAOYCRCQC5hx8l6JzSgtNLeW43HXGPvy0BfCJobqsd8F1PC0kU-pTEuOhVb97rx7fxUf8VQ5GEp0IvmNrKxeJ0vIqij9s1yEf_RIA3WY63JrkeLKyW5nvTRWbW73c4XM8UNZaS5Jiu5wlyyj1M9eTQfhpW9QztlvnWPssiBg2cp31aca1MkUi_OQtXfDkII4Svg0v20xjMOeexWhTN_jtJ0V9GjgYBSou8B2iaMzIv-hawQL5hE77luW6ted23YOcxu-CBmQa9LnrsrqwzTlrkYHkygNnLqteI0zNPtHtx8v4QLdfP3uR0_89lcUMuvAWcwDwwKTBKbLc6iO4KBrU1iyqPIZgBfOyAQnt9nseTvGopaHVFHISe3pQHnuGOix8CQieKeT69WE1hr0Dmd4U7cYEQ9sf4WCp6bfxxS-eIwvbilzIUqnWuv0kwLZzn4L5uhyTjirYgwMnz9SKFD73ePkvaTl5uWXaCTNH86FrTFPLB6-X7GE0CmEdGqN6j9wmTZxQ0hjL6CZDAObwsRUmWSoPZnkE-I-RUhkiiDqTYrMOmhmoPlAP9HXYU1bS8TSklV8ZcHuqVD8OfFcufS-N93s5f0H6S_DZSpFzbeyZuBcTEnc_T8jvYNq4XpgbYe4BN1EEWGZypC57A3WkoOHljH_D-kuBzv0ITa8ZLDptVuHQTbr8oYffNlw%3D%3D',
   'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ld4qx0YVkhCGk95BHaDHeU0mv6uDOh2O2ipjZo6NoleOFP3uDtc3FQBSvTz00HRezP6M12PoS3qF-BqoAYx72wrrh28EnIkoBp3K3HFMp8mGIU-nrSkrPPyPbKpQkemAHzLlKKlkAaBWqC4RjH3j6kZtSfkhgkCbUbXcfrn7oIQ7IQBBYaZdf_rs9sHVL5u5tHCXqnIteXU7_9ELcnO6p6aWuQbujag6qtaK8usbCFqOzuNM4nBHXnbrMgga0Fb3_lZh4y5t6Qmn-P2q8vjE3yFQlbqzvgtyGAeR1oWQ_wFyC1LU4tXtkM2MvP6n2HpObQDE4KpBJnMXQEBHuF16P4rSrvupXvL7-Thi7ShB4rol2kQE4STDhsIEIWc1x-NhZeU0Bx-mpm4A0jXSGjr7NmklWLS6vUTp4BQRKNHpvOeEt3m_sv5iVL7ca65ezG3q3HjHcC78sXHPc36Mkr5-f3GiTQcA37FCMiluwJh2wJRWP5aKHLGpAnJVviSCOiHV9Nn9WXJ2s7tkdIRaHSUjD3AiYmTxEuEw3Jy9a-nOl41HSqI6KmOCUsIuH0VVcJSVvO2pe7OjLxxvVDTXkCSNOYtJ36XhWEtoil_3tYuUw16L_oBrD3_Kl5fOQQjw7obHSZDtKrWF2pmQcjRTRfGphR6JMhFD93no3xs6RH1fwhv2qFpwsMoYmq6pqQV4zEz-1PuCAsgtI4_Oac8UyDa9XbyiFXV_h_Tz2mDcoumZMB8TJ9lMLpN1s4-QhRksv-r-YUNEgkWnUb2wjreTVa2BLZUExBd5oqlwhxiA4cX4wXbsRxqjWdFrFZ',
   'YOUTH_WITHDRAWBODY': ''
}



COOKIELIST = [cookies1,]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    redBodyVar = f'YOUTH_REDBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and redBodyVar in os.environ and os.environ[redBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies'+str(i + 1)]["YOUTH_REDBODY"] = os.environ[redBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers):
  """
  分享文章
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://focu.youth.cn/article/s?signature=QqvZWbEKpA2yrNR1MnyjPetpZpz2TLdDDw849VGjJl8gXB5keP&uid=52242968&phone_code=4aa0b274198dafebe5c214ea6097d12b&scid=35438728&time=1609414747&app_version=1.8.2&sign=17fe0351fa6378a602c2afd55d6a47c8'
  readUrl = 'https://focus.youth.cn/article/s?signature=QqvZWbEKpA2yrNR1MnyjPetpZpz2TLdDDw849VGjJl8gXB5keP&uid=52242968&phone_code=4aa0b274198dafebe5c214ea6097d12b&scid=35438728&time=1609414747&app_version=1.8.2&sign=17fe0351fa6378a602c2afd55d6a47c8'
  try:
    response1 = requests_session().post(url=url, headers=headers, timeout=30)
    print('分享文章1')
    print(response1)
    time.sleep(0.3)
    response2 = requests_session().post(url=readUrl, headers=headers, timeout=30)
    print('分享文章2')
    print(response2)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account['YOUTH_HEADER']
    readBody = account['YOUTH_READBODY']
    redBody = account['YOUTH_REDBODY']
    readTimeBody = account['YOUTH_READTIMEBODY']
    withdrawBody = account['YOUTH_WITHDRAWBODY']
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    shareArticle(headers=headers)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    # article_red_res = articleRed(body=redBody)
    # if article_red_res:
    #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
