# coding:utf-8
"""
    自用快捷代码工具
    作者：罗航宇 
    邮箱:lhyweb@gmail.com
    https://pypi.python.org/pypi/icbc
    安装方法：pip install icbc
    使用方法：
    import icbc
    z=icbc.tool()  
    简要版本记录 :
    20140701 整合近几年代码，制作zen_ie,zen_tool
    20141209 制作pip包
    20150102 添加zen_gui
    20150411 移除串口功能和pygame的引用
    20150412 重构
    20150724 zen_tool优化filter_flist中多参数支持
    20150808 zen_tool添加log模块
    20150815 zen_tool添加序列化、反序列化功能
    20150815 添加线程池功能zen_thread_pool, 修正zen_tool中的time_mili问题
    20150815 zen_tool优化，重命名部分方法
    20150815 由zen_lib变更名称为icbc,重新注册pypi
    20150826 zen_ie改为类,支持同时操控多个网页
    20150926 zen_thread_pool添加线程池gui显示、控制功能
    20150926 zen_tool优化性能，修复bug
    20150927 zen_tool修改list_file,filter_filetype的bug，简单实现kvdict
    20151118 zen_tool添加kv_dict,zip,sha1,base64、get_ip，用户名等一系列功能
    20151127 zen_tool添加了加载程序等很多功能
    20151128 icbc添加了程序服务器
    20151129 zen_tool添加了file_ext,file_name,优化filter_filetype等涉及list遍历的方法
    20151130 zen_tool添加了system,taskkill,暂仅win可用，优化logging,logging未测试
    20151130 zen_ie增加一系列功能
    20151201 zen_tool添加encode，decode的私有加解密方法
    20151211 zen_tool移除zip、unzip压缩和解压缩功能，
    20151211 zen_tool添加socks5协议
    20151211 zen_tool添加load_xls和save_xls,实现list与xls之间的互转，基于xlrd和xlwt(用于xls自动填ie表格)
    20160103 zen_tool移除单例模式，适配sae和gae使用
    20160111 zen_tool重构为函数形式（zen_tool_class为旧版，停止更新新功能）
    20160118 zen_ie完善功能
    20160122 zen_gui增加图标、zen_tool增加文件转io对象功能
    20160129 添加ssdp协议，局域网内快速识别服务器
    20160129 添加zen_net,整合网络相关代码
    20160316 完善zen_app的expire，计划移除部分代码
    20160501 zen_tool增加z的引用方式,用法from icbc import z
    20160501 增加zen_gui的print重定向
    20160507 优化zen_gui的print重定向，增加多个程序图标
    20160507 优化zen_gui的置顶显示和icon代码
    20161211 zen_key增加key_up,key_down mouse_up,mouse_down
    20161211 zen_key重构为函数方式，并更名为zen_con，停止维护zen_key
    20161212 zen_con添加键盘鼠标监控功能,初步实现，计划增加回调接口
    20161215 zen_tool增加write_txt,replace、decodes多个功能
    20180803 适配python3
    20181129 全面适配python3.7，不再兼容pyhon2，版本号调整为2.0
    20200919 完善多个bug
    TODO:
    编写文档
    修改log模块
    增加ssdp协议
    增加json配置读写 已完成
"""
def version():
    
    return 201610
def gui(title="", is_top=False):
    """
    简单图形控制器界面
    an easy GUI tool for control your program
    
    gui_demo=icbc.gui(title=u"test", is_top=True)

    gui_demo.mainloop()
    """
    from .import zen_gui
    tk_gui = zen_gui.zen_gui(title, is_top)
    return tk_gui
def thread_pool(size=5, is_gui=False):
    """
    线程池
    import icbc
    import time
    def test(t1,t2):
        print t1
        time.sleep(4)
        print t2
    tp=icbc.thread.pool(size=5,is_gui=True)
    tp.start()
    for i in range(100):
        tp.add(test,(i，i))
     
    """
    from .import zen_thread_pool
    return zen_thread_pool.thread_pool(size, is_gui)
def key():
    """
    仅Windows可用,模拟键盘鼠标操作
    key=icbc.key()
    
    """
    from .import zen_key
    key_control = zen_key.zen_key()
    return key_control
def ie():
    """
    仅Windows可用,控制ie操作
    """
    from .import zen_ie
    ie = zen_ie.zen_ie()
    return ie
def file_server(folder):
    """上传文件
    """
    from .import zen_net
    zen_net.file_server(folder)
def remote_server(folder=None, port=8888, need_convert=False, secret=""):
    """
    start http server for suply remote python code 
    开启一个远程服务器，提供py代码
    """
    from .import zen_app
    zen_app.start_serving(folder, port, need_convert, secret)
def remote_run(remote_url="http://127.0.0.1:8888/?app=not found", secret=""):
    """
    launch remote python code from http_server
    执行远程服务器的代码
    """
    from . import zen_app
    zen_app.app_run(remote_url, secret=secret)

def doc():
    """"查看当前文档
    """
    from . import zen_tool
    zen_tool.pydoc(package="icbc")

