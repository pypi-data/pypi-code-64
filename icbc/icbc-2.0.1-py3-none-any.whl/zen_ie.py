# -*- coding: utf-8 -*-
try:
    from win32com.client import DispatchEx
except ImportError:
    input("only for windows, need pywin32(http://sourceforge.net/projects/pywin32/)")
    
import time
"""
仅限windows可用
"""
ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
class zen_ie():
    ie = None
    
    def __init__(self):
        self.ie = None
    def new_ie(self, url=None):
        self.ie = DispatchEx("InternetExplorer.Application")
        if url:
            self.ie.Navigate(url)
    def get_ie(self):
        return self.ie
    def get_doc(self):
        return self.ie.Document
    def get_body(self):
        return self.ie.Document.body
    def set_visible(self, is_visible=True):
        if is_visible:
            self.ie.Visible = 1
        else:
            self.ie.Visisble = 0
    def get_url(self):
        return self.ie.LocationURL
    def open(self, url):
        self.ie.Navigate(url)
    def quit(self):
        self.ie.Quit()
        
    def get_title(self):
        return self.ie.Document.title
    def get_outer_text(self, node=None):
        if node == None:
            self.wait_ie()
            doc = self.ie.Document
            body = doc.body
            data = body.outerText
        else:
            data = node.outerText
        return data
    def search_ie(self, url_keys=["http://exam/wis18/usermain/paper/userpaper.answeruserpapercurr.flow?sid=", "http://exam/wis18/usermain/main/paper.builduserpapercurr.flow?sid="], is_show=False):
        ie = None
        if isinstance(url_keys, str):
            url_keys = [url_keys]
            
        apps = DispatchEx(ShellWindowsCLSID)
        for i in apps:
            if type(url_keys) == type("") or type(url_keys) == type(""):
                for j in url_keys:
                    if i.LocationURL.count(j) > 0:
                        if is_show:
                            print(("IE match,key=", url_keys))
                        ie = i  
            elif type(url_keys) == type([]):
                for j in url_keys:
                    if i.LocationURL.count(j) > 0:
                        if is_show:
                            print(("IE match,key=" + j))
                        ie = i            
        apps = None
        self.ie = ie
        if ie == None:
            time.sleep(0.7)
            if is_show:
                print(("No matched IE:", url_keys))
            self.search_ie(url_keys, is_show)
        return ie

        
    def wait_ie(self):
        while self.ie.Busy:
            time.sleep(0.25)
    def find(self, tag, nodeattr=None, nodeval=None, nodeattr2=None, nodeval2=None):
        if nodeattr == None:
            pass
        elif isinstance(nodeval, list):
            for i in nodeval:
                i = self.decode(i)
        else:
            nodeval = self.decode(nodeval)
        if nodeattr2 == None:
            pass
        elif isinstance(nodeval2, list):
            for i in nodeval2:
                i = self.decode(i)
        elif not isinstance(nodeval2, str):
            nodeval2 = self.decode(nodeval2)
        return self.get_elements(self.ie.Document, tag, nodeattr, nodeval, nodeattr2, nodeval2)
    def decode(self, sss_in, coding="utf-8"):
        if isinstance(sss_in, str):
            return sss_in
        else:
            return sss_in.decode(coding)
    def get_elements(self, doc, tag, nodeattr=None, nodeval=None, nodeattr2=None, nodeval2=None):
        """
        内部函数
        """
        result = []
        self.wait_ie()
        body = doc.body
        for node in body.getElementsByTagName(tag):
            if nodeattr == None:
                result.append(node)
                
            elif nodeattr2 == None:
                # 单参数
                if isinstance(nodeval, list):
                    # 单参数多值
                    if nodeval.count(node.getAttribute(nodeattr)) > 0:
                        result.append(node)
                    
                elif node.getAttribute(nodeattr) == nodeval:
                    # 单参数唯一值
                    result.append(node)
            elif isinstance(nodeval, list) and isinstance(nodeval2, list):
            # 双参数多值    
                if nodeval.count(str(node.getAttribute(nodeattr))) > 0 and nodeval2.count(node.getAttribute(nodeattr2)) > 0:
                    result.append(node)
            else:
            # 双参数均单值
                if str(node.getAttribute(nodeattr)) == nodeval and str(node.getAttribute(nodeattr2)) == nodeval2:
                    result.append(node)
                    
        frames = doc.frames
        if frames.length > 0:
            for i in range (frames.length):
                doc_in = frames[i].Document
                tmp = self.get_elements(doc_in, tag, nodeattr, nodeval, nodeattr2, nodeval2)
                if not tmp == []:
                    for e in tmp:
                        result.append(e) 
        return result

    def get_nodes(self, parentNode, tag):
        childNodes = []
        for childNode in parentNode.getElementsByTagName(tag):
            childNodes.append(childNode)
        return childNodes
    def get_node_by_attr(self, Nodes, nodeattr, nodeval):
        for node in Nodes:
            if str(node.getAttribute(nodeattr)) == nodeval:
                return node
        return None
    def set_node(self, node, html_val):
        node.innerHTML = html_val
if __name__ == "__main__":
    ie = zen_ie()
    ie.search_ie(["baidu.com"])
    t = ie.find("input", "id", "su", "type", "submit")
    print((t[0].value))
    t[0].value = time.ctime()
