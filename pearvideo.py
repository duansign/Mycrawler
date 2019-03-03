import requests,re,os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

base_url = "https://www.pearvideo.com/"


def get_index():
    res = requests.get(base_url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "referer": "https: // www.baidu.com / link?url = fUq54ztdrrLaIUXa - p6B9tuWXC3byFJCyBKuvuJ_qsPw8QLrWIfekFKGgmhqITyF & wd = & eqid = c5366da10000199a000000025c45768a"
    })

    return res.text



def parser_index(text):
    urls = re.findall('<a href="(.*?)" class="vervideo-lilink actplay">',text)
    urls = [base_url + i for i in urls]
    return urls


def get_details(url):
    res=requests.get(url)
    # print(res.status_code)
    # print(res.text)
    return res.text


def parser_details(text):
    video_url = re.search(r'srcUrl="(.*?\.mp4)"',text).group(1)

    title = re.search('<h1 class="video-tt">(.*?)</h1>',text).group(1)

    content = re.search('<div class="summary">(.*?)</div>', text).group(1)

    date = re.search('<div class="date">(.*?)</div>', text).group(1)

    count = re.search('<div class="fav" data-id=".*?">(.*?)</div>', text).group(1)

    # print(video_url,title,content,date,count)
    return {"video_url":video_url,"title":title,"content":content,"date":date,"count":count}


def download_video(url,title):
    data = requests.get(url)

    if not os.path.exists("videos"):
        os.makedirs("videos")
    filename = os.path.join("videos",title)+".mp4"
    filename = filename.replace(":","_")
    with open(filename,"wb") as f:
        f.write(data.content)
    print("%s download finished..."%title)




if __name__ == '__main__':
    pool = ThreadPoolExecutor(5)
    data = get_index()
    urls = parser_index(data)
    for i in urls:
        t = get_details(i)
        dic = parser_details(t)
        # download_video(dic['video_url'],dic['title'])
        pool.submit(download_video,dic['video_url'],dic['title'])
        print("submit task",dic["title"])
    print("submit finished!")













