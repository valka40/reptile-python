#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# @Description: 获取虚拟信息
# @PreInstall: 
# @Author : https://www.bajins.com
# @File : FictitiousInfo.py
# @Version: 1.0.0
# @Time : 2019/12/26/026 12:10
# @Project: reptile-python
# @Package: 
# @Software: PyCharm
import re

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/72.0.3626.109 Safari/537.36 "
}

haoweichi_url = {
    # 美国
    "usa": "http://www.haoweichi.com",
    # 加拿大
    "canada": "http://www.haoweichi.com/Others/jia_na_da_shen_fen_sheng_cheng",
    # 澳大利亚
    "australia": "http://www.haoweichi.com/Others/ao_da_li_ya_ren_shen_fen_sheng_cheng",
    # 法国
    "france": "http://www.haoweichi.com/Others/fa_guo_ren_shen_fen_sheng_cheng",
    # 意大利
    "italy": "http://www.haoweichi.com/Others/yi_da_li_ren_shen_fen_sheng_cheng",
}


def get_haoweichi(url):
    result = BeautifulSoup(requests.get(url, timeout=600).text, headers=headers, features="lxml")
    parent = result.select("body > div.container.index > div.row.main-left > "
                           "div.col-md-9.col-sm-9.col-xs-12.no-margin.no-padding > div > div.row.no-margin")

    parent = parent[0].find_all("input")

    data = {
        # 全名
        "full_name": parent[0].attrs["value"],
        # 性别
        "gender": parent[1].attrs["value"],
        # 名字
        "first_name": parent[2].attrs["value"],
        # 姓
        "last_name": parent[3].attrs["value"],
        # 中间名
        "middle_name": parent[4].attrs["value"],
        # 称呼
        "call": parent[5].attrs["value"],
        # 生日
        "birthday": parent[6].attrs["value"],
        # 州
        "State": parent[7].attrs["value"],
        # 街道地址
        "street_address": parent[8].attrs["value"],
        # 城市
        "city": parent[9].attrs["value"],
        # 电话
        "phone": parent[10].attrs["value"],
        # 邮编
        "postcode": parent[11].attrs["value"],
        # 州全称
        "full_state_name": parent[12].attrs["value"],
        # SSN社会保险号
        "ssn_social_security_number": parent[13].attrs["value"],
        # 临时邮箱
        "temporary_mailbox": parent[14].attrs["value"],
        # 网络用户名
        "network_username": parent[15].attrs["value"],
        # 随机密码
        "random_code": parent[16].attrs["value"],
        # 信用卡类型
        "credit_card_type": parent[17].attrs["value"],
        # 信用卡号
        "credit_card_number": parent[18].attrs["value"],
        # CVV2
        "cvv2": parent[19].attrs["value"],
        # 有效期
        "expiration_date": parent[20].attrs["value"],
        # 职位（职称）
        "position ": parent[21].attrs["value"],
        # 所属公司
        "affiliates ": parent[22].attrs["value"],
        # 身高
        "height ": parent[23].attrs["value"],
        # 体重
        "body_weight ": parent[24].attrs["value"],
    }

    return data


def get_fakenamegenerator(url, params):
    result = BeautifulSoup(requests.get(url, params, headers=headers, timeout=600).text, features="lxml")
    parent = result.select("#details > div.content > div.info > div")[0]

    # 替换<br/>为-
    _address = parent.select("div.address > div")[0].get_text("-", strip=True).split(",")
    address = _address[0].split("-")
    data = {
        "full_name": parent.select("div.address > h3")[0].text,
        "address": address[0],
        "city": address[1],
        "zip_code": _address[1],
    }
    extras = parent.find_all("dl")
    for extra in extras:
        dt = extra.find("dt")
        dd = extra.find("dd")
        content = dd.text
        # 替换除字母数字空格以外的内容
        name = re.sub(r"[^a-z\d\s]", "", dt.text, 0, re.I)
        # 替换空格并转小写
        name = re.sub(r"\s", "_", name, 0, re.I).lower()
        if name == "email_address":
            email = re.sub(r"\s.*$", "", dd.text, 0, re.I)
            href = dd.find("a").attrs["href"]
            content = f"{email} {href}"
        if name == "phone":
            if content.find('-') == -1:
                data["area_code"] = ""
            else:
                data["area_code"] = content[:content.find('-')]
            content = content[content.find('-') + 1:]
        if name == "qr_code":
            continue
        # 去掉开头或者结尾空白字符
        data[name] = re.sub(r"^\s+|\s+$", "", content, 0, re.I)

    return data


def get_fakenamegenerator_index(params=None):
    if params is None:
        params = {
            # 姓名命名的国家
            "n": "us",
            # 国家：ca、us
            "c": "ca",
            # 性别：random、male、female
            "gen": "random",
        }
    return get_fakenamegenerator("https://www.fakenamegenerator.com/index.php", params)


def get_fakenamegenerator_advanced(params=None):
    if params is None:
        params = {
            "t": "country",
            # 数组多选，最多5个
            "n[]": "us",
            # 数组多选，最多5个
            "c[]": "us",
            "gen": "78",
            "age-min": "19",
            "age-max": "32",
        }
    return get_fakenamegenerator("https://www.fakenamegenerator.com/advanced.php", params)


if __name__ == '__main__':
    print(get_fakenamegenerator_index())

    # print(get_fakenamegenerator_advanced())
