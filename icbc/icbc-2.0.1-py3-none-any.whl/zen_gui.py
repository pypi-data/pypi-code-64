# -*- coding:utf-8 -*-
"""
20150412 重构
20150512 重构为类
20151130 增加一些新功能
20160501 增加print接收
20180317 增加canvas、labelentry等功能，修正部分bug
"""
from builtins import isinstance
try:
    import tkinter
    import sys
    import time
except ImportError:
    input("import Tkinter error")
class StdoutRedirector():
    def __init__(self):
        self.var = tkinter.StringVar()
        self.var.set("")
        self.console = sys.stdout
        self.buffer = []
    def write(self, ssss):
        self.console.write(ssss)
        if not ssss == "\n":
            self.buffer.append(ssss)
            
            if len(self.buffer) > 25:
                tmp = self.buffer[-25:]
            else:
                tmp = self.buffer
            result = ""
            for i in tmp:
                    result = result + "\n>" + i
            self.var.set(result[1:])
    def save(self, filename):
        f = open(filename, "a")
        for i in self.buffer:
            f.write(i)
        f.close()
        self.buffer = []
    def reset(self):
        sys.stdout = self.console
class zen_gui():
    root = ""
    dict_hotkey = ""
    is_top = False
    icon_dict = {"icbc":"icon_icbc.ico",
                "sync": "icon_sync.ico",
                "config":"icon_config.ico",
                 0:"icon_config.ico",
                "default":"icon_icbc.ico"}
    def get_root(self):
        return self.root
    def set_hotkey_handler(self, hotkey_proc):
        """
        Demo 
        def hotkey_proc(event):
            tmp = event.char
            if tmp == "n":
                show_next()
            elif tmp == "h":
                copyto_best()
        """
    
        self.root.bind("<Key>", hotkey_proc)
    def show_print(self, is_print=True, style="white-black", after=None):
        if is_print:
            if self.is_print:
                return
            self.frame_show = tkinter.Frame(self.root, borderwidth=1, bg=style.split("-")[0], relief=tkinter.RIDGE)
            self.frame_show.pack(side=tkinter.RIGHT, after=after, fill=tkinter.BOTH)
            sys.stdout = StdoutRedirector()
            self.message = tkinter.Message(self.frame_show, textvariable=sys.stdout.var, width=1000, relief=tkinter.RAISED, fg=style.split("-")[1], bg=style.split("-")[0])
            self.message.grid(sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)
        else:
            if self.is_print:
                self.frame_show.destroy()
        self.is_print = is_print
            
    def __init__(self, title_name="Undefined Title", is_top=False, icon=0):
        self.root = tkinter.Tk(className=title_name)
        self.frame_left = tkinter.Frame(self.root, borderwidth=1, relief=tkinter.RIDGE)
        self.frame_left.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.dict_hotkey = {}
        self.show_top(is_top)
        self.is_print = False
        self.icon = icon
    def set_icon(self, icon=None):
        if icon == None:
            icon = self.icon
        if icon in self.icon_dict:
            if __file__.count("zen_gui.pyc"):
                icon = __file__.replace("zen_gui.pyc", self.icon_dict[icon])
            else:
                icon = __file__.replace("zen_gui.py", self.icon_dict[icon])
            self.root.iconbitmap(icon)
        else:
            print ("icon error")
    def set_title(self, title):
        self.root.title(title)
    def show_top(self, is_top=True):
        self.is_top = is_top
        if self.is_top:
            self.root.wm_attributes("-topmost", 1)
    def add_hotkey(self, key="n", event=None):
        if event == None:
            self.dict_hotkey[key] = msgbox
        else:
            self.dict_hotkey[key] = event
    def exit(self):
        self.root.destroy()
    def show(self):
        self.root.deiconify()
    def hide(self):
        self.root.withdraw()
    def msgbox(self, show_title="Undefined Message Title", show_str="Undefined Message Text"):
        import tkinter.messagebox
        return tkinter.messagebox.showinfo(show_title, show_str)
    def inputbox(self, title="Undefined Inputbox Title", prompt="Undefined Prompt"):
        import tkinter.simpledialog
        return tkinter.simpledialog.askstring(title=title, prompt=prompt)
    def add_button(self, bt_name="Undefined button Name", new_function=msgbox, width=20, height=2):
        varstr = tkinter.StringVar()
        varstr.set(bt_name)
        tmp_button = tkinter.Button(self.frame_left,
                anchor="center",  # 指定文本对齐方式
                textvariable=varstr,  # 指定按钮上的文本
                width=width,  # 指定按钮的宽度，相当于40个字符
                height=height,
                command=new_function)  # 指定按钮的高度，相当于5行字符
        tmp_button.text = varstr
        tmp_button.get_text = varstr.get
        tmp_button.set_text = varstr.set
        tmp_button.pack()
        return tmp_button
    def add_checkbox(self, text="text", onvalue=1, offvalue=0, event=None):
        """
        ss=gui.add_checkbox()
        ss.get()    
        """
        varstr = tkinter.StringVar()
        varstr.set(text)
        variable = tkinter.IntVar()
        variable.set(0)
        tmp_check_button = tkinter.Checkbutton(self.frame_left,
            variable=variable,
            textvariable=varstr,
            onvalue=onvalue,  # 设置On的值
            offvalue=offvalue,  # 设置Off的值
            command=event)
        
        tmp_check_button.get_value = variable.get
        tmp_check_button.set_value = variable.set
        tmp_check_button.get_text = varstr.get
        tmp_check_button.set_text = varstr.set
        tmp_check_button.pack()
        return tmp_check_button
        
    def add_label(self, show_str="Undefined Label"):
        """
wraplength：    指定多少单位后开始换行
justify:        指定多行的对齐方式
ahchor：        指定文本(text)或图像(bitmap/image)在Label中的显示位置
布局如下图

                nw        n        ne
                w      center    e
                sw        s        se
'''
        """
        varstr = tkinter.StringVar()
        varstr.set(show_str)
        label = tkinter.Label(self.frame_left, textvariable=varstr, wraplength=240, justify='left')
        label.pack()
        label.get_text = varstr.get
        label.set_text = varstr.set
        return label
    def add_entry(self, show_str="", width=20):
        varstr = tkinter.StringVar()
        varstr.set(show_str)
        en = tkinter.Entry(self.frame_left, textvariable=varstr, width=width)
        en.pack()
        en.get_text = varstr.get
        en.set_text = varstr.set
        return en
    def add_label_entry(self, label_str="", entry_str="", width=20, ratio=0.3):
        frame = tkinter.Frame(self.frame_left, relief=tkinter.RIDGE)
        varstr = tkinter.StringVar()
        varstr.set(entry_str)
        label = tkinter.Label(frame, text=label_str, width=int(width * ratio) - 1, wraplength=240, justify='left')
        en = tkinter.Entry(frame, textvariable=varstr, width=width - int(width * ratio))
        en.get_text = varstr.get
        en.set_text = varstr.set
        label.pack(side=tkinter.LEFT)
        en.pack(side=tkinter.LEFT)
        frame.pack()
        return en
    def add_canvas(self, width=640, height=480, bg="white"):
        canvas = tkinter.Canvas(self.root,
                                width=width,  # 指定Canvas组件的宽度
                                height=height,  # 指定Canvas组件的高度
                                bg=bg)  # 指定Canvas组件的背景色
        canvas.pack(side=tkinter.LEFT)
        return canvas
    
    def chooser_directory(self, title="Folder Chooser文件夹选择器"):
        import os
        import tkinter.filedialog
        tmp_path = tkinter.filedialog.askdirectory(title=title)
        if tmp_path == "":
            return ""
        else:
            return tmp_path.replace("/", os.sep) + os.sep
        
    def chooser_file_open(self, title="File Chooser文件选择器", file_type='*.txt *.zen'):  # 按钮事件处理函数
        import tkinter.filedialog
        r = tkinter.filedialog.askopenfilename(title=title,  # 创建打开文件对话框
                filetypes=[('zen_data', file_type), ('All files', '*')])  # 指定文件类型为Python脚本
        return r  # 输出返回值
    def chooser_file_save(self, title='Output Choose', initialdir=r'D:\\', initialfile='ouput_data.txt'):  # 按钮事件处理函数
        import tkinter.filedialog
        r = tkinter.filedialog.asksaveasfilename(title=title, initialdir=initialdir, initialfile=initialfile)
        return r
    def chooser_color(self, title="Zen Color Choose"):  # 按钮事件处理函数
        import tkinter.colorchooser
        r = tkinter.colorchooser.askcolor(title=title)  # 创建颜色选择对话框
        print(r)
        return r  # 输出返回值
    def mainloop(self):
        self.set_icon()
        self.root.mainloop()
def _demo_test_thread(ee):
    for i in range(1000):
        ee.set_text(str(i))
        time.sleep(1)
def _demo_hotkey_proc(event):
    tmp = event.char
    print(tmp)
    if tmp == "h":
        gui_demo.hide()
    elif tmp == "q":
        gui_demo.exit()
    elif tmp == "s":
        gui_demo.show()
def ttt(sss="print and switch icon"):
    gui_demo.set_icon(0)
    print(sss)
if __name__ == "__main__":
    from icbc import z
    gui_demo = zen_gui("ZenGUIDemo", is_top=True)
    qqq = gui_demo.add_button("动态添加新按钮", lambda:gui_demo.add_button("随机按钮"))
#     qqq.destroy()
    gui_demo.add_button("颜色选择器", gui_demo.chooser_color)
    gui_demo.add_button("测试选择目录", gui_demo.chooser_file_open)
    gui_demo.add_button("测试选择写入文件", gui_demo.chooser_file_save)
    gui_demo.add_button("测试选择写入目录", gui_demo.chooser_directory)
    gui_demo.add_button("退出gui", gui_demo.exit)
    gui_demo.add_button("隐藏gui", gui_demo.hide)
    gui_demo.add_button("显示gui", gui_demo.show)
    gui_demo.add_button("测试显示", lambda:gui_demo.show_print())
    gui_demo.add_button("测试退出", lambda:gui_demo.show_print(False))
    gui_demo.add_button("测试print", ttt)
    gui_demo.add_label_entry("标题", "测试内容")
    gui_demo.set_hotkey_handler(_demo_hotkey_proc)
    gui_demo.add_canvas()
    gui_demo.show_top()
    gui_demo.show_print(style="blue-yellow")
    label_test = gui_demo.add_label("测试label2")
    label_test.set_text("测试label")
    checkbox_test1 = gui_demo.add_checkbox("测试选择按钮")
    checkbox_test2 = gui_demo.add_checkbox("测试选择按钮2")
    entry_test = gui_demo.add_entry()
    entry_test.set_text("测试写入entry")
    z.new_thread(_demo_test_thread, (entry_test,))  # 测试变量
    gui_demo.mainloop()
