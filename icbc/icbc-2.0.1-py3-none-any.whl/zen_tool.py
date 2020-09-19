# coding:utf-8

import os
import time
from setuptools.package_index import ContentChecker
debug_level = 5
sep=os.sep
def folder_name(folder):
    return folder[folder.rfind(os.sep)+1]
def beep():
    print ("\a")
def argv():
    import sys
    return sys.argv
def params():
    import sys
    return sys.argv
def command(command):
    """not work
    run command in terminal or cmd,todo"""
    import subprocess
    subprocess.call([command])
def system(command):
    """
    use cmd
    """
    commands = command.replace("\r", "\n").split("\n")
    for command in commands:
        if len(command) > 1:
            os.system(command)
def secret_calc(secret="str"):
    sec_int = 0
    for i in base64_encode(secret):
        sec_int = sec_int + ord(i)
    return sec_int
    
def encode(str, secret_key=""):
    str = base64_encode(str)
    secret_int = secret_calc(secret_key) % len(str)
    str_new = str[secret_int:] + str[0:secret_int]
    return str_new
def decode(str, secret_key=""):
    secret_int = secret_calc(secret_key) % len(str)
    secret_int = len(str) - secret_int
    str = str[secret_int:] + str[0:secret_int]
    str = base64_decode(str)
    return str

    
    
def taskkill(program=["python.exe", "pythonw.exe"]):
    """kill task"""
    if exists("taskkill.exe"):
        cmd_template = "taskill /f /im %s"
    elif exists("C:/Windows/System32/taskkill.exe"):
        cmd_template = "C:/Windows/System32/taskkill.exe /f /im %s\n"
    elif exists("C:/Windows/SysWOW64/taskkill.exe"):
        cmd_template = "C:/Windows/SysWOW64/taskkill.exe /f /im %s\n"
    else:
        dbp("taskkill not work")
        return None
    if isinstance(program, str):
        program = [program]
    for i in program:
        os.system(cmd_template % i)
def exec_code (code, area=globals()):
    """run python code
    todo"""
    if isinstance(code, str):
        exec(code, area)

def dbp(*params):
    "if debug_flag: print title,content"
    if debug_level > 0:
        print (*params)
        
def get_clipboard():
    """get text from clickboard
    """
    if is_win():
        import win32clipboard
        import win32con
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
    else:
        import subprocess
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
    return data
def set_clipboard(str):
    """set text into clickboard
    """
    if is_win():
        import win32clipboard
        import win32con
        time.sleep(0.05)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, str)
        win32clipboard.CloseClipboard()
    else:
        import subprocess
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(str)
        p.stdin.close()
        retcode = p.wait()  
        
def is_win():
    "to detect if system is win"
    import platform
    sysstr = platform.system()
    if sysstr .count("Windows") > 0:
        return True
    else:
        return False
# log 功能            
def log_init(filename="log.txt"):
    "开启log功能，默认是log.txt,此处得优化 todo"
    import logging
    logging.basicConfig(level=logging.DEBUG,
                format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                datefmt="%Y%m%d %H:%M:%S",
                filename="log.txt",
                filemode="a")

def log(message, level=0):
    "logging.error(message)"
    import logging
    if level == 2:
        logging.error(message)
    elif level == 1:
        logging.warning(message)
    else:
        logging.warning(message)
# 数据读取功能
def load_data(filename, sep=None):
    "读取文件，并每行按tab分列，然后返回list"
    f = open(filename, "r")
    tmp = []
    if sep == None:
        for i in f:
            tmp.append(i)
    else:
        for i in f:
            tmp.append(i.split("\t"))
    f.close()
    return tmp
def load_txt(filename):
    "读取文本文件"
    content = False
    if os.path.exists(filename) and os.path.isfile(filename):
        f = open(filename, "r")
        try:
             content = f.read()
        finally:
             f.close()
    return content
def write_txt(filename, content, encoding=None,mode="w"):
    "写入文本文件"
    f = open(filename, mode,encoding=encoding)
    f.write(content)
    f.close()
    
def load_xls(filename, sheet_id=0):
    "读取xls文件，第二参数是工作表序号"
    import xlrd
    tmp = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[sheet_id]  # 通过索引顺序获取
    nrows = table.nrows
    for i in range(nrows):
          tmp.append(table.row_values(i))
    return tmp
def save_xls(filename, data, sheet_title="sheet1", encoding="utf-8"):
    import xlwt
    w = xlwt.Workbook(encoding)
    ws = w.add_sheet(sheet_title)
    for y in range(len(data)):
        for x in range(len(data[y])):
            ws.write(y, x, data[y][x])
def replace(content, replace_dict):
    "对字符串进行批量替换"
    for i in replace_dict:
        if content.count(i):
            content.replace(i, replace_dict[i])
    return content
def detect(str):
    "判断文字编码"
    import chardet
    result = chardet.detect(str)
    dbp(result)
    return result
def decodes(content, codings=["gbk", "utf-8"], test=False):
    "对常见编码进行解码"
    if isinstance(content, str):
        return content
        
    for i in codings:
        try:
            content = content.decode(i)
        except:
            pass
        else:
            return content
    if test:
        print(content)
        print(detect(content))

# 时间、格式功能
def fmt(time_current=None, time_format="%Y%m%d_%H%M%S"):
    "时间字符串生成: 20150819_102959"
    if time_current == None:
        time_current = time.time()
    return time.strftime (time_format, time.localtime(time_current))
def fmt_mili(time_format="%Y%m%d_%H%M%S_"):
    "生成时间字符串,格式:20161230_101111_321"
    time_current = time.time()
    return fmt(time_current, time_format) + str(time_current % 10)[2:5]
def fmt_decode(time_string, time_format="%Y%m%d_%H:%M:%S"):
    "时间字符串解码,默认格式:%Y%m%d_%H:%M:%S"
    return time.mktime(time.strptime (time_string, time_format))
def fmt_delta(time_string1, time_string2, time_format="%Y%m%d_%H%M%S"):
    "时间字符串计算时间差，默认格式%Y%m%d_%H%M%S"
    return time.mktime(time.strptime (time_string2, time_format)) - time.mktime(time.strptime (time_string1, time_format))
def fmt_convert(time_string, format_from, format_to):
    "时间字符串计算时间差，默认格式%Y%m%d_%H%M%S"
    return time.strftime(format_to, time.strptime (time_string, format_from))
def date(time_current=None):
    return fmt(time_current, "%Y%m%d")
def second():
    return int(time.time())
def sleep(t=0.1):
    "等待x秒"
    time.sleep(t)
    
# 单独功能
def random(end=100, start=0):
    "产生随机数"
    import random
    return random.randint(start, end)
def new_thread(function_name, function_params=(), delay=0):
    import threading
    "创建新线程，不纳入线程池管理，多个参数，function_params以tuple或list包装起来"
    if not (isinstance(function_params, tuple) or isinstance(function_params, list)):
        function_params = (function_params,)
    if delay > 0:
        thread_tmp = threading.Thread(target=thread_pack, args=(time.sleep, (delay,), function_name, function_params))
    else:
        thread_tmp = threading.Thread(target=function_name, args=function_params)
    thread_tmp.start()
    return thread_tmp
def thread_pack(func, params=(), func2=None, params2=()):
    func(*params)
    if not func2 == None:
        func2(*params2)
def image_format(filename):
    "获取图片格式，todo 添加错误处理"
    try:
        from PIL import Image
    except:
        import Image
    return Image.open(filename).format
def grab(filename=None):
    "截图并保存到当前文件夹下，自动命名为当前时间毫秒"
    try:
        from PIL import ImageGrab
    except:
        import ImageGrab
    img = ImageGrab.grab()
    if filename == None:
        filename = fmt_mili()
    img.save(filename + ".png", "PNG")
def md5(string):
    """calculate md5 for string
    计算字符串md5"""
    from hashlib import md5
    m = md5()
    m.update(string)
    return m.hexdigest()
def base64_encode(str, times=1):
    """base64_encode"""
    import base64
    tmp = str
    while times > 0:
        times = times - 1
        tmp = base64.encodestring(tmp)
    return tmp
        

    
def base64_decode(str, times=1):
    """base64_decode"""
    import base64
    tmp = str
    while times > 0:
        times = times - 1
        tmp = base64.decodestring(tmp)
    return tmp
def md5_file(filename):
    """calculate md5 for file
    计算文件md5"""
    from hashlib import md5
    m = md5()
    f = open(filename, 'rb')
    m.update(f.read())
    f.close()
    return m.hexdigest()
def sha1(string):
    """calculate sha1 for string
    计算字符串sha1"""
    from hashlib import sha1
    return sha1(string).hexdigest()
def sha1_file(filename):
    """calculate sha1 for file
    计算文件sha1"""
    from hashlib import sha1
    s = sha1()
    f = open(filename, 'rb')
    s.update(f.read())
    f.close()
    return s.hexdigest() 
#     def mp3_play( filename="r:\\1.mp3"):
#         import pygame
#         pygame.mixer.init()
#         pygame.mixer.music.load(filename)
#         pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy():
    #    m = pygame.mixer.music.get_pos()
    #    print m
    #    time.sleep(0.1)
def tts_speak(word="语音功能成功加载"):
    """调用tts说话"""
    # 需windows下使用
    if is_win():
        global tts_windows
        try:
            tts_windows.tts_speak(word)
        except:
            from win32com.client import DispatchEx
            tts_windows = DispatchEx("SAPI.SpVoice")
            tts_windows.speak(word)
    else:
        try:
            os.system("say " + word)
        except:
            pass
def browse(url="www.bing.com"):
    import webbrowser
    webbrowser.open(url)
def pydoc(port=random(50000, 10000), package=None):
    """展示pydoc"""
    import pydoc
    if port < 2000:
        random(50000, 10000)
    if package == None:
        package = ""
    else:
        package = "/" + package + ".html"
    url = "http://127.0.0.1:" + str(port) + package
    new_thread(browse, url)
    dbp (url)
    dbp("已写入粘贴版，请直接再浏览器打开")
    set_clipboard(url)
    try:
        pydoc.serve(port)
    except:
        dbp("端口被占用，尝试使用其他端口")
        pydoc()
def debug(func, params=None, is_pause=True, is_log=False):
    "debug"
    
    try:   
        if params == None:
            func()
        elif isinstance(params, list):
            func(params)
        elif isinstance(params, tuple):
            func(params)
        else:
            tmp = (params)
            func(tmp)
             
    except:
        import traceback
        traceback.print_exc()
        if is_log:
            f = open("debug_log.txt", 'a')
            f.write("\n#################" + z.fmt() + "#################\n")
            traceback.print_exc(file=f)
            f.write("\n#################" + z.fmt() + "#################\n")
            f.flush()   
            f.close()
        
        if is_pause:
            z.sleep(0.5)
            input("-------z.debug:found error,press any key to continue------")
            
        
# 文件、筛选目录功能
def list_file(folder=os.getcwd(), filetype=None, is_fullpath=False):
    """获取文件列表，可添加格式list筛选"""
    tmp = os.listdir(folder)
    if is_fullpath:
        result = [os.path.join(folder, i) for i in tmp if os.path.isfile(os.path.join(folder, i))]
    else:
        result = [i for i in tmp if os.path.isfile(os.path.join(folder, i))]
    if not filetype == None:
        "过滤文件类型"
        result = filter_filetype(filetype, result)
    return result

def list_file_all(folder=os.getcwd(), filetype=None, is_fullpath=False):
    """列举所有文件"""
    result = []
    if is_fullpath:
        for root, dirs, files in os.walk(folder):
            for ff in files:
                result.append(os.path.join(root, ff))
    else:
        for root, dirs, files in os.walk(folder):
            for ff in files:
                result.append(ff)
    if not filetype == None:
        """过滤文件类型"""
        result = filter_filetype(filetype, result)
    return result
def list_folder(folder=os.getcwd(),is_fullpath=False):
    """获取文件列表，可添加格式list筛选"""
    tmp = os.listdir(folder)
    result = []
    for i in tmp:
        if os.path.isdir(os.path.join(folder, i)):
            if is_fullpath:
                result.append(os.path.abspath(i))
            else:
                result.append(i)
    return result
def list_folder_all(folder=os.getcwd()):
    """获取文件夹下全部文件夹"""
    result = []
    for i in os.walk(folder):
        if os.path.isdir(i[0]):
            result.append(i[0] + os.sep)
    return result
def filter_filetype(file_type, data):
    """
    对list过滤文件类型
    flist=filter_filetype(["txt"],filelist)
    """
    
    if isinstance(file_type, str):
        file_types = ["." + file_type]
    elif isinstance(file_type, list):
        file_types = ["." + i for i in file_type if isinstance(i, str)]
    else:
        file_types = []
    return [i for i in data if file_ext(i) in file_types]
def file_ext(filename):
    "取得拓展名"
#         dot_pos = filename.rfind(".")
#         return filename[dot_pos:] if 0 < dot_pos < (len(filename) - 1) > 1 else ""todo 测试哪种更快
    return os.path.splitext(filename)[1]
def file_name(filename):
    "去除拓展名"
    return os.path.splitext(filename)[0]
def join(*p):
    """os.path.join()todo test and fix"""
    return os.path.join(*p)
def getcwd():
    """取得当前工作路径todo test and fix"""
    return os.getcwd()
def dirname(p):
    return os.path.dirname(p)
def copy(old, new):
    """复制文件todo test and fix"""
    import shutil
    shutil.copy(old, new)
def move(old, new):
    """移动文件todo test and fix"""
    os.rename(old, new)
def rename(old, new):
    """重命名文件todo test and fix"""
    os.rename(old, new)
def delete(filename):
    """删除文件todo test and fix"""
    os.remove(filename)
def remove(filename):
    """删除文件todo test and fix"""
    os.remove(filename)
def chdir(path=os.getcwd()):
    """修改当前路径"""
    os.chdir(path)
def chmod(file, mode=0o777):
    """修改指定文件权限，默认权限0o777"""
    os.chmod(file, mode)
def abspath(filename=""):
    """获取绝对路径"""
    return os.path.abspath(filename)
def exists(filename):
    """判断文件是否存在"""
    return os.path.exists(filename)
def isdir(filename):
    """判断是否目录"""
    return os.path.isdir(filename)
def folder(path=""):
    """判断是否路径是否存在目录，否则自动新建该目录"""
    path = abspath(path)
    if not os.path.exists (path):
        path_parent = os.path.split(path)[0]
        if not path == path_parent:
            folder(path_parent)
        os.mkdir(path)
    return path
def get_ip():
    """取得本机ip"""
    import socket
    hostname = socket.gethostname()  
    ip = socket.gethostbyname(hostname)
    return ip
def get_hostname():
    """取得本机hostname"""
    import socket
    hostname = socket.gethostname()  
    return ip

# 存储、读取功能
def save(obj, filename=None):
    "序列化保存"
    import pickle
    if filename == None:
        return pickle.dumps(obj)
    else:
        f = open(filename, "wb")
        pickle.dump(obj, f, -1)
        f.close()
def loads(dump_string):
    "序列化读取"
    import pickle
    return pickle.loads(dump_string)
def load(filename):
    "序列化读取"
    import pickle
    try:
        if exists(filename):
            f = open(filename, "rb")
            result = pickle.load(f)
            f.close()
        else:
            result = {}
            dbp (filename, "不存在，返回空词典")
    except:
        import traceback
        traceback.print_exc()
        result = {}
        dbp (filename, "该文件无法读取或者有错误，返回空词典")
        
    return result
def json_loads(json_string):
    import json
    return json.loads(json_string)
def json_dumps(data):
    import json
    return json.dumps(data)


def kv_get(key):
    """key-value get 使用前kv_init"""
    global kvdict
    if kvdict == None:
        dbp ("kv_dict not init")
        return None
    if key in kvdict:
        return kvdict[key]
    else:
        return None
def kv_put(key, value):
    """key-value put 使用前kv_init"""
    global kvdict, kvdict_filename
    if kvdict == None:
        dbp("kv_dict not init")
        return None
    kvdict[key] = value
    save(kvdict, kvdict_filename)
def kv_init(filename):
    """key-value init"""
    global kvdict_filename, kv_dict
    kvdict_filename = filename
    kvdict = load(filename)
def is_open(ip="127.0.0.1", port=80):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False
def main_menu(ddd):
    print ("please select funcion to run:")
    for i in range (len(ddd)):
        print (i, ddd[i].__name__, ddd[i])
    choice = int(input("choice:"))
    ddd[choice]()
def ramfile(filename=None):
    from io import StringIO
    class ramfile(StringIO):
        def open(self, filename, mode):
            f = open(filename, mode)
            try:
                self.write(f.read())
            finally:
                f.close()
            self.io.seek(0)
        def save(self, filename, mode):
            self.seek(0)
            f = open(filename, mode)
            try:
                f.write(self.read())
            finally:
                f.close()
    if filename:
        f = open(filename, "rb")
        try:
             tmpIO.write(f.read())
        finally:
             f.close()
    return tmpIO

def qrcode(content, filename=None):
    import qrcode
    q = qrcode.main.QRCode() 
    q.add_data(content) 
    q.make() 
    img = q.make_image() 
    if filename == None:
        from io import StringIO
        tmpIO = StringIO()
        img.save(tmpIO)
        return tmpIO
    else:
        img.save(filename)
        return filename
def main():
    dbp("zen_tool: " + fmt_mili())
    dd = []
    dd.append(pydoc)
    dd.append(main_menu)
    dd.append(beep)
    dd.append(lambda: tts_speak("tts测试"))
    main_menu(dd)
if __name__ == "__main__":
    print (fmt_mili(""))
    main()
