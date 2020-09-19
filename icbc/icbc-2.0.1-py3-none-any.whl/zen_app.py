# coding:utf-8
from . import z
def expire(user_code="", serial_code="", cert_file=None):
    """to detect if python app is expired"""
    result = True
    if isinstance(cert_file, str) :
        cert_obj = z.load(cert_file)
        user_code = cert_obj["user_code"]
        serial_code = cert_obj["serial_code"]
    user_code = user_code + z.format_time(time_format="%Y")
    if isinstance(serial_code, str) :
        if z.md5(user_code) == serial_code:
            result = False
    elif isinstance(serial_code, list) :
        for i in serial_code:
            if z.md5(user_code) == i:
                result = False
    if result:
        count = list(range(4))
        count.reverse()
        for i in count:
            z.sleep(1)
            print(("授权错误：证书超期\n%s秒后自动退出" % i))
        exit()
def gen_cert(user_code):
    if isinstance(user_code, list):
        cert = []
        for i in user_code:
            cert.append(z.md5(i))
        return cert
    elif isinstance(user_code, str):
        return z.md5(user_code)
    else:
        return ""
def gen_cert_file():
    cert = {}
    cert["user_code"] = "user_code"
    cert["serial_code"] = "serial_code"
    cert["expire_date"] = "20151211"
    cert["times_limit"] = "user_code"
    cert["last_date"] = "20151231"
    cert["last_date"] = "20151231"
    pass
def app_run(url=None, filename=None, cwd=None, secret=""):
    """run python app from file or internet"""
    if cwd == None:
        cwd = z.getcwd()
    z.chdir(cwd)
    if not filename == None:
        code = z.load_txt(filename)
    elif not url == None:
        import urllib.request, urllib.parse, urllib.error
        if url.count("http://") < 1:
            url = base64_decode(url)
        code = urllib.request.urlopen(url).read()
    else:
        return "None"
    code = z.decode(code, secret)
    z.exec_code(code)
def app_gen(file_in, file_out=None, secret=""):
    """make app from py file"""
    code = z.load_txt(file_in)
    code = z.encode(code, "")
    if file_out == None:
        file_out = file_in + ".app"
    f = open(file_out, "w")
    f.write(code)
    f.close()
    return code
def start_serving(folder=None, port=8888, need_convert=False, convert_secret=""):
    import tornado.ioloop
    import tornado.web
    if folder == None:
        folder = z.getcwd()
        
    class app_handler(tornado.web.RequestHandler):
        def get(self):
            key = self.get_argument('app', '')
            if key in app_dict:
                result = app_dict[key]
            else:
                result = app_dict["NOT MATCH"]
    
            self.write(result)
        def post(self):
            self.write("None")
    global app_dict
    app_dict = {}
    if need_convert:
        apps = z.list_file(folder, filetype="py")
        for i in apps:
            app_dict[i.split(".")[0]] = z.encode(z.load_txt(i), convert_secret)
        
    else:
        apps = z.list_file(folder, filetype="app")
        for i in apps:
            app_dict[i.split(".")[0]] = z.load_txt(i)
    app_dict["NOT MATCH"] = z.encode("print ('requested app is not found')", convert_secret)
    server = "http://%s:%s/?app=" % (z.get_ip(), str(port))
    print("[app server]:", server)
    print("[app folder]:", folder)
    print("[app count]:", len(app_dict))
    for i in app_dict:
        print(server + i)
    z.set_clipboard(server)
    app = tornado.web.Application([
        (r"/", app_handler),
    ])
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == "__main__":
    expire("sdf", gen_cert("sdf2016"))
#     start_serving(os.getcwd(), 8888, True)

    

