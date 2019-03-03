import requests
import re
import pyecharts



user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
res = requests.get("https://www.lagou.com/",headers = {"User-Agent":user_agent})
# print(res.status_code)
# print(res.text)

data = re.search("<span>后端开发</span>([\s\S]*?)后端开发其它</a>",res.text).group(1)
data = data.replace(" ","").replace("\n","")
urls = re.findall('<ahref="(.*?)"data-lg-tj-id="4O00"data-lg-tj-no="01\d\d"data-lg-tj-cid="idnull"class=".*?">(.*?)</a>',data)
print(urls)


def parser_job(i):
    # 工作的链接
    job_url = re.search('href="(.*?)"', i).group(1)
    name = re.search("<h3>(.*?)</h3>", i).group(1)
    add = re.search("<em>(.*?)</em>", i).group(1)
    money = re.search('"money">(.*?)</span>', i).group(1)
    jy, xl = re.search('-->([\s\S]*?)\n', i).group(1).split(" / ")

    return {"name":name,"add":add,"job_url":job_url,"money":money,"jy":jy,"xl":xl}

# 指定需要查看的技术方向
jobs = ["Java","Python"]

# 创建一个页面
page = pyecharts.Page()
for url in urls:
    if url[1] not in jobs:
        continue

    # 存储解析完成的字典
    datas = []

    for j in range(1,6):
        res = requests.get(url[0] + str(j))
        data = re.findall("""<a class="position_link"([\s\S]*?)<div class="company">""",res.text)
        for i in data:
            dic = parser_job(i)
            if "{" in dic["xl"]:
                continue
            datas.append(dic)
    print(len(datas))
    # 统计每个起薪有多少个岗位
    count_dic = { }
    for d in datas:
        key = d["money"].split("-")[0]
        if key in count_dic:
            count_dic[key] += 1
        else:
            count_dic[key] =1
    print(url[1],count_dic)

    # 创建一个饼图
    pie = pyecharts.Pie()
    # 为饼图添加数据
    """
    标题
    keys
    values
    """
    pie.add(url[1],count_dic.keys(), count_dic.values())
    # 将图加到页面上
    page.add(pie)


# 生成一个页面文件
page.render("test.html")








