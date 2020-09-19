# coding:utf-8
import urllib.request, urllib.error, urllib.parse
from icbc import z
def post(url, post_data):
    try:
        req_data = post_data.encode("utf-8")
    except:
        req_data = post_data
    request = urllib.request.Request(url, req_data)
    response = urllib.request.urlopen(request)
    return response.read()
    
def get(url):
    response = urllib.request.urlopen(url)
    return response.read()

def push_web(server, key, web):
    "note:only for gae api,web"
    result = {"api":"web", "key":key, "content":web, "permission":"icbc", "action" : "push"}
    result = z.json_dumps(result)
    post(server, result)

def tornado_server(port=8888):
    import tornado.ioloop
    import tornado.web
    class main_handler(tornado.web.RequestHandler):
        def get(self):
            print(self.get_argument(''))
            self.write("get")
        def post(self):
            client_ip = self.request.remote_ip
            for i in  self.request.arguments:
                print(i)
            s = self.get_arguments("body")
            print(s)
            self.write("post")
    application = tornado.web.Application([(r"/", main_handler), ])
    application.listen(port)
    print("start web")
    tornado.ioloop.IOLoop.instance().start()
def file_server(filepath, url=r"/file" , port=8031):
    import tornado.ioloop
    import tornado.web
    class UploadFileHandler(tornado.web.RequestHandler):
        def get(self):
            self.write('''
            <html>
            <head>
                <title>Upload File</title>
                <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.2/jquery.mobile-1.3.2.min.css">
                <script src="http://code.jquery.com/mobile/1.3.2/jquery.mobile-1.3.2.min.js"></script>
                </head>
              <body>
                <form action='file' enctype="multipart/form-data" method='post'>
                <input type='file' name='file'/><br/>
                <input type='submit' value='submit'/>
                </form>
              </body>
            </html>''')
        def post(self):
            file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
            for meta in file_metas:
                filename = meta['filename']
                filename_save = z.join(filepath, filename)
                with open(filename_save, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
                self.write(filename + ' finished!')
    address = "http://%s:%d%s" % (z.get_ip() , port, url)
    print(address)
    z.set_clipboard(address)
    app = tornado.web.Application([
        (url, UploadFileHandler),
    ])
     
    if __name__ == '__main__':
        app.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    
def push_web():
    z.sleep(2)
    print("start demo")
    push_web("http://127.0.0.1:8888/", "test", "ttttttttttttt")
def test_tornado_server():
    z.new_thread(demo)
    tornado_server()
def test_file_server():
    file_server("/Users/l/code/test/")
if __name__ == "__main__":
    print(z.getcwd())
    file_server(z.getcwd())
