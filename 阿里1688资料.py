from tkinter import messagebox
import requests, re
from bs4 import BeautifulSoup
import tkinter
from tkinter.constants import CURRENT
# import sys
# import os


# 设置绝对路径
# def get_ico_src(relative_src):
#     if getattr(sys, "frozen", False):
#         base_path = sys._MEIPASS
#     else:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_src)
# icon_src=get_ico_src(os.path.join("resources","versioncuecs2.ico"))


class MainForm():
    def __init__(self):
        # 设置一个页面
        self.root = tkinter.Tk()        
        # 设置页面总标题
        self.root.title('啦啦啦专属')
        # 界面logo
        self.root.iconbitmap(icon_src)
        # 设置窗口
        self.win()
        # 设置背景颜色
        self.root["background"] = "orange"
        # 输入处理
        self.text()
        self.root.mainloop()

    def win(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width - 500) / 2
        y = (self.screen_height - 90) / 2
        # 设置居中窗口
        self.root.geometry("500x90+%d+%d" % (x, y))
        # 禁止修改窗体
        self.root.resizable(width=False,height=False)

    def text(self):
        self.content = tkinter.StringVar()
        self.entry = tkinter.Entry(
            self.root,
            width=50,
            textvariable=self.content,
            font=(
                '微软雅黑',
                20))
        self.button = tkinter.Button(
            self.root, text='确定', fg="black", font=(
                "微软雅黑", 12))
        self.button.bind('<Button-1>', self.task)
        self.entry.pack()
        self.button.pack()

      # 主程序
    def task(self, event):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
            "cookie": "保密，自己设"
        }
        search_url = self.entry.get()
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        try:
            data = soup.find("ul", class_="nav-tabs").find_all("li")
        except:
            messagebox.showerror("错误提示", "网址选择错误!!!")
            self.root.protocol("WM_DELETE_WINDOW", self.root.destroy())
        obj_01 = re.compile(r'"original":"(.*?)"}', re.S)
        for photo_url in data:
            # li标签 , class="tab-trigger"属性 , data-imgs文件位置
            result_url = obj_01.findall(photo_url.get("data-imgs"))
            # print(result_url[0])
            file_01 = result_url[0].split("ibank/")[-1]
            file_name = file_01.replace("/", "p")
            # print(file_name)
            try:
                result_res = requests.get(result_url[0])
                with open(file_name, mode="wb") as f:
                    f.write(result_res.content)
            except:
                messagebox.showerror("错误提示", "下载失败!!!")
                self.root.protocol("WM_DELETE_WINDOW", self.root.destroy())
        messagebox.showinfo("温馨提示", "下载完成!!!")
        self.content.set("")



if __name__ == "__main__":
    MainForm()
