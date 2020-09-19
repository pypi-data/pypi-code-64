# coding:utf-8
import threading
import time
class thread_pool():
    """
    线程池功能
    tp = thread_pool(5)
    for i in range(10):
        tp.add(func, [i])
        
        
    todo:
    强制终止线程
    优化线程池的方法
    
    """
    queue = []
    process_flag = False
    running_flag = False
    thread_max_size = 5
    running_count = 0
    error_list = []
    def __init__(self, size=5, is_gui=False):
        self.thread_max_size = size
        self.running_flag = False
        self.gui_flag = is_gui
        # thread.start_new(self.loop, ())
        if is_gui:
            self.gui()
        handler_loop = threading.Thread(target=self.loop, args=())
        handler_loop.start()
    def gui(self):
        import zen_gui
        self.gui = zen_gui.zen_gui("线程池控制器")
        self.et1 = self.gui.add_label(u"test")
        self.et2 = self.gui.add_label(u"test")
        self.et3 = self.gui.add_label(u"test")
        self.gui.add_button("启动处理队列", self.start)
        self.gui.add_button("暂停处理队列", self.stop)
        self.gui.add_button("清空等待队列", self.clear_queue)
        self.gui.add_button("清空当前队列", self.clear_running)
        guimainloop = threading.Thread(target=self.gui.mainloop, args=())
        guimainloop.start()
    def loop(self):
        "控制线程"
        while True:
            if self.process_flag:
                print "queue_size:", len(self.queue), "running_count:", self.running_count, "error_count", len(self.error_list)
            if self.gui_flag:
                self.et1.set_text("Queen:%d" % (len(self.queue)))
                self.et2.set_text("Running:%d" % (self.running_count))
                self.et3.set_text("Error:%d" % (len(self.error_list)))
            if not self.running_flag:
                time.sleep(1)
                continue
            if len(self.queue) > 0 and self.running_count < self.thread_max_size:
                thread_pack_params = self.queue.pop(0)
                # thread.start_new_thread(self.thread_pack, function_params)
                thread_tmp = threading.Thread(target=self.thread_pack, args=thread_pack_params)
                thread_tmp.start()
                self.running_count = self.running_count + 1
            else:
                time.sleep(0.9)


    def start(self):
        "开启线程"
        self.running_flag = True
    def stop(self):
        "停止线程"
        self.running_flag = False
    def clear_queue(self):
        "清空线程队列"
        self.queue = []
    def clear_running(self):
        "清空线程队列,todo重写线程类，添加强行中止线程功能"
        self.running_count = 0
    def add(self, function_name, function_params=(), callback=None, callback_params=()):
        "添加到线程序列"
        self.queue.append((function_name, function_params, callback, callback_params))
    def switch(self, tof=False):        
        "是否显示记录"
        self.process_flag = tof
    def get_count_queue(self):
        return len(self.queue)
    def get_count_error(self):
        return len(self.error_list)
    def get_count_running(self):
        return self.running_count
    def thread_pack(self, func, params=(), callback=None, callback_params=()):
        "内部函数"
        try:
            func(*params)
            if not callback == None:
                callback(*callback_params)
        except:
            print ("thread_pack error")
            import traceback
            traceback.print_exc()
            self.error_list.append((func, params, callback, callback_params))
        finally:
            self.running_count = self.running_count - 1
def _demo_function(tag):
    print tag, u"线程开始,5秒后结束"
    time.sleep(5)
    print tag, u"线程结束"
    
if __name__ == "__main__":
    tp = thread_pool(3, is_gui=True)
    for i in range(10):
        tp.add(_demo_function, (i,))
    tp.start()
        
    
    
