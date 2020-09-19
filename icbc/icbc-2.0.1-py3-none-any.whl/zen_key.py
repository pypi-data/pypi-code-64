# -*- coding: utf-8 -*-
try:
    import win32clipboard
    import win32con
    import win32api
    import win32gui
    from ctypes import *
except ImportError:
    eval(input("only for windows, need pywin32(http://sourceforge.net/projects/pywin32/)"))
import time
class zen_key():
    """
    仅限windows可用
    201506整合进zen_lib
    201508重构为类，增加鼠标操控
    20151205修改粘贴板bug，增加剪切、复制、粘贴、删除、alt+tab程序替换（switch）
    """
    def __init__(self):
        pass
    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        d = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        return d
    def set_clipboard(self, aString):
        time.sleep(0.05)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)
        win32clipboard.CloseClipboard()
    def single_key(self, keycode):
        time.sleep(0.05)
        win32api.keybd_event(keycode, 0, 0, 0)  # v键位码是86
        time.sleep(0.05)
        win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0) 
    def multi_key(self, keycodes=[86, 12]):
        time.sleep(0.05)
        for keycode in keycodes:
            win32api.keybd_event(keycode, 0, 0, 0)
        time.sleep(0.05)
        for keycode in keycodes:
            win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0) 
    def paste(self):
        """CTRL+V 
        CTRL:17 
        V:86"""
        self.multi_key([17, 86])
    def copy(self):
        """CTRL+C
        CTRL:l17
        C:67"""
        self.multi_key([17, 67])
    def cut(self):
        """CTRL+C
        CTRL:l17
        X:88"""
        self.multi_key([17, 88])
    def delete(self):
        self.send_key(127)
    def tab(self):
        self.single_key(9)
    def switch(self):
        self.multi_key([18, 9])
    def backspace(self):
        self.single_key(8)
    def enter(self):
        self.single_key(13)
    def space(self):
        self.single_key(32)
        
    def press(self, string):
        if len(string) > 1:
            for i in string:
                self.single_key(ord(i))
        elif len(string) == 1:
            self.single_key(ord(string))
            
    def mouse_click (self, x, y):
        windll.user32.SetCursorPos(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
        time.sleep(0.3)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)
    def mouse_getpos(self):
        return win32gui.GetCursorPos()
    def ascii(self):
        print ("""Dec    Hex    缩写/字符    解释    
0    0    NUL(null)    空字符    
1    1    SOH(start of headline)    标题开始    
2    2    STX (start of text)    正文开始    
3    3    ETX (end of text)    正文结束    
4    4    EOT (end of transmission)    传输结束    
5    5    ENQ (enquiry)    请求    
6    6    ACK (acknowledge)    收到通知    
7    7    BEL (bell)    响铃    
8    8    BS (backspace)    退格    
9    9    HT (horizontal tab)    水平制表符    
10    0A    LF (NL line feed, new line)    换行键    
11    0B    VT (vertical tab)    垂直制表符    
12    0C    FF (NP form feed, new page)    换页键    
13    0D    CR (carriage return)    回车键    
14    0E    SO (shift out)    不用切换    
15    0F    SI (shift in)    启用切换    
16    10    DLE (data link escape)    数据链路转义    
17    11    DC1 (device control 1)    设备控制1    
18    12    DC2 (device control 2)    设备控制2    
19    13    DC3 (device control 3)    设备控制3    
20    14    DC4 (device control 4)    设备控制4    
21    15    NAK (negative acknowledge)    拒绝接收    
22    16    SYN (synchronous idle)    同步空闲    
23    17    ETB (end of trans. block)    传输块结束    
24    18    CAN (cancel)    取消    
25    19    EM (end of medium)    介质中断    
26    1A    SUB (substitute)    替补    
27    1B    ESC (escape)    换码(溢出)    
28    1C    FS (file separator)    文件分割符    
29    1D    GS (group separator)    分组符    
30    1E    RS (record separator)    记录分离符    
31    1F    US (unit separator)    单元分隔符    
32    20    (space)    空格    
33    21    !    　    
34    22    "    　    
35    23    #    　    
36    24    $    　    
37    25    %    　    
38    26    &    　    
39    27    '    　    
40    28    (    　    
41    29    )    　    
42    2A    *    　    
43    2B    +    　    
44    2C    ,    　    
45    2D    -    　    
46    2E    .    　    
47    2F    /    　    
48    30    0    　    
49    31    1    　    　
50    32    2    　    　
51    33    3    　    　
52    34    4    　    　
53    35    5    　    　
54    36    6    　    　
55    37    7    　    　
56    38    8    　    　
57    39    9    　    　
58    3A    :    　    　
59    3B    ;    　    　
60    3C    <    　    　
61    3D    =    　    　
62    3E    >    　    　
63    3F    ?    　    　
64    40    @    　    　
65    41    A    　    　
66    42    B    　    　
67    43    C    　    　
68    44    D    　    　
69    45    E    　    　
70    46    F    　    　
71    47    G    　    　
72    48    H    　    　
73    49    I    　    　
74    4A    J    　    　
75    4B    K    　    　
76    4C    L    　    　
77    4D    M    　    　
78    4E    N    　    　
79    4F    O    　    　
80    50    P    　    　
81    51    Q    　    　
82    52    R    　    　
83    53    S    　    　
84    54    T    　    　
85    55    U    　    　
86    56    V    　    　
87    57    W    　    　
88    58    X    　    　
89    59    Y    　    　
90    5A    Z    　    　
91    5B    [    　    　
92    5C    \    　    　
93    5D    ]    　    　
94    5E    ^    　    　
95    5F    _    　    　
96    60    `    　    　
97    61    a    　    　
98    62    b    　    　
99    63    c    　    　
100    64    d    　    　
101    65    e    　    　
102    66    f    　    　
103    67    g    　    　
104    68    h    　    　
105    69    i    　    　
106    6A    j    　    　
107    6B    k    　    　
108    6C    l    　    　
109    6D    m    　    　
110    6E    n    　    　
111    6F    o    　    　
112    70    p    　    　
113    71    q    　    　
114    72    r    　    　
115    73    s    　    　
116    74    t    　    　
117    75    u    　    　
118    76    v    　    　
119    77    w    　    　
120    78    x    　    　
121    79    y    　    　
122    7A    z    　    　
123    7B    {    　    　
124    7C    |    　    　
125    7D    }    　    　
126    7E    ~    　    　
127    7F    DEL (delete)    删除""")
if __name__ == "__main__":
    zk = zen_key()
    zk.press("r")
    
