import requests
import re
import hashlib
from parsel import Selector
from fontTools.ttLib import TTFont
from urllib import parse

url = 'http://www.porters.vip/confusion/movie.html'
resp = requests.get(url)
sel = Selector(resp.text)

# 获取未加密的电影信息
movie_data = sel.css("div.movie-brief-container").css("::text").extract()
# 去除不需要的空白字符
for i in movie_data:
    if "".join(i.split()):    
        print("".join(i.split()))

# 提取页面加载的所有css文件路径
css_path = sel.css('link[rel=stylesheet]::attr(href)').extract()
woffs = []
# 拼接movie.css链接，请求获取、拼接woff链接
for c in css_path:
    # 拼接css链接
    css_url = parse.urljoin(url, c)
    css_resp = requests.get(css_url)
    # 匹配需要的woff链接
    woff_path = re.findall("src:url\('..(.*.woff)'\) format\('woff'\);", css_resp.text)
    # 路径存在则执行
    if woff_path:
        woffs += woff_path

# 请求、下载woff文件
woff_url = 'http://www.porters.vip/confusion' + woffs.pop()
woff = requests.get(woff_url)
with open('movie.woff', 'wb') as f:
    f.write(woff.content)

# 自定义字典
base_font = [{"name": "uniEE76", "value": "0", "hex": "fc170db1563e66547e9100cf7784951f"},
             {"name": "uniF57B", "value": "1", "hex": "251357942c5160a003eec31c68a06f64"},
             {"name": "uniE7DF", "value": "2", "hex": "8a3ab2e9ca7db2b13ce198521010bde4"},
             {"name": "uniF19A", "value": "3", "hex": "712e4b5abd0ba2b09aff19be89e75146"},
             {"name": "uniF593", "value": "4", "hex": "e5764c45cf9de7f0a4ada6b0370b81a1"},
             {"name": "uniEA16", "value": "5", "hex": "c631abb5e408146eb1a17db4113f878f"},
             {"name": "uniE339", "value": "6", "hex": "0833d3b4f61f02258217421b4e4bde24"},
             {"name": "uniE9C7", "value": "7", "hex": "4aa5ac9a6741107dca4c5dd05176ec4c"},
             {"name": "uniEFD4", "value": "8", "hex": "c37e95c05e0dd147b47f3cb1e5ac60d7"},
             {"name": "uniE624", "value": "9", "hex": "704362b6e0feb6cd0b1303f10c000f95"}]

font = TTFont('movie.woff')
# 解密函数
def translate(code):
        for i in base_font:
            code_glyf = font["glyf"].glyphs.get(code).data
            code_md5 = hashlib.md5(code_glyf).hexdigest()
            if code == i.get("name") and code_md5 == i.get("hex"):
                return i.get("value")

# 使用正则提取字体编码
code_re = re.compile('<span class="stonefont">(.*?)</span>')
chi_re = re.compile(u'[\u4e00-\u9fa5]+')
font_data = code_re.findall(resp.text)

# 处理、解密字体编码，解密结果添加进列表
font_list = []
for i in range(len(font_data)):
    words = ''
    for x in font_data[i].upper().split("&#X"):
        for y in x.split("."):
            if y:
                if chi_re.search(y):
                    words+=translate("uni"+y[:-1])
                else:
                    words+=translate("uni"+y)
    font_list.append(words)

print(f"评分：{font_list[0][0]}.{font_list[0][-1]}  评分人数：{font_list[1][:-1]}.{font_list[1][-1]}万人")
print(f"累计票房：{font_list[-1][:-2]}.{font_list[-1][-2:]}亿")
