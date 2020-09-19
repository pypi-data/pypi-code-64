# -*- coding: utf-8 -*-
try:
    import win32clipboard
    import win32con
    import win32api
    import win32gui
    from ctypes import *
except ImportError:
    input("only for windows, need pywin32(http://sourceforge.net/projects/pywin32/)")
import time
"""
    仅限windows可用
    201506整合进zen_lib
    201508重构为类，增加鼠标操控，增加粘贴板读写
    20151205修改粘贴板bug，增加剪切、复制、粘贴、删除、alt+tab程序替换（switch）
    20161211增加key_up,key_down mouse_up,mouse_down
    20161211重构为函数方式，zen_key更名为zen_con
    20161212添加键盘鼠标监控功能,初步实现，计划回调借口
"""
def __init__():
    pass
def get_clipboard():
    win32clipboard.OpenClipboard()
    d = win32clipboard.GetClipboardData(win32con.CF_TEXT)
    win32clipboard.CloseClipboard()
    return d
def set_clipboard(aString):
    time.sleep(0.05)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)
    win32clipboard.CloseClipboard()
def get_windowsw_name():
    HWND = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(HWND)
def key_down(keycode):
    win32api.keybd_event(keycode, 0, 0, 0)
def key_up(keycode):
    win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0)
def single_key(keycode):
    time.sleep(0.05)
    win32api.keybd_event(keycode, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0) 
def multi_key(keycodes=[86, 12]):
    time.sleep(0.05)
    for keycode in keycodes:
        win32api.keybd_event(keycode, 0, 0, 0)
    time.sleep(0.05)
    for keycode in keycodes:
        win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0) 
def paste():
    """CTRL+V 
    CTRL:17 
    V:86"""
    multi_key([17, 86])
def copy():
    """CTRL+C
    CTRL:l17
    C:67"""
    self.multi_key([17, 67])
def cut():
    """CTRL+C
    CTRL:l17
    X:88"""
    self.multi_key([17, 88])
def delete():
    self.send_key(127)
def tab():
    self.single_key(9)
def switch():
    self.multi_key([18, 9])
def backspace():
    self.single_key(8)
def enter():
    self.single_key(13)
def space():
    self.single_key(32)
    
def press(string):
    if len(string) > 1:
        for i in string:
            self.single_key(ord(i))
    elif len(string) == 1:
        self.single_key(ord(string))
def set_mouse_pos(x, y):
    windll.user32.SetCursorPos(x, y)
def get_mouse_pos():
    return win32gui.GetCursorPos()
def mouse_click (x, y):
    mouse_down(x, y)
    time.sleep(0.3)
    mouse_up(x, y)
def leftclick_down(pos=None):
    if pos == None:
        pos = get_mouse_pos()            
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1])
def leftclick_up(pos=None):
    if pos == None:
        pos = get_mouse_pos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1])
def rightclick_down(pos=None):
    if pos == None:
        pos = get_mouse_pos()            
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos[0], pos[1])
def rightclick_up(pos=None):
    if pos == None:
        pos = get_mouse_pos()
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos[0], pos[1])
ascii = """Dec(十进制)	Hex(十六进制)	缩写/字符	解释
0	0	NUL(null)	空字符
1	1	SOH(start of headline)	标题开始
2	2	STX (start of text)	正文开始
3	3	ETX (end of text)	正文结束
4	4	EOT (end of transmission)	传输结束
5	5	ENQ (enquiry)	请求
6	6	ACK (acknowledge)	收到通知
7	7	BEL (bell)	响铃
8	8	BS (backspace)	退格
9	9	HT (horizontal tab)	水平制表符
10	0A	LF (NL line feed, new line)	换行键
11	0B	VT (vertical tab)	垂直制表符
12	0C	FF (NP form feed, new page)	换页键
13	0D	CR (carriage return)	回车键
14	0E	SO (shift out)	不用切换
15	0F	SI (shift in)	启用切换
16	10	DLE (data link escape)	数据链路转义
17	11	DC1 (device control 1)	设备控制1
18	12	DC2 (device control 2)	设备控制2
19	13	DC3 (device control 3)	设备控制3
20	14	DC4 (device control 4)	设备控制4
21	15	NAK (negative acknowledge)	拒绝接收
22	16	SYN (synchronous idle)	同步空闲
23	17	ETB (end of trans. block)	结束传输块
24	18	CAN (cancel)	取消
25	19	EM (end of medium)	媒介结束
26	1A	SUB (substitute)	代替
27	1B	ESC (escape)	换码(溢出)
28	1C	FS (file separator)	文件分隔符
29	1D	GS (group separator)	分组符
30	1E	RS (record separator)	记录分隔符
31	1F	US (unit separator)	单元分隔符
32	20	(space)	空格
33	21	!	叹号
34	22	"	双引号
35	23	#	井号
36	24	$	美元符
37	25	%	百分号
38	26	&	和号
39	27	'	闭单引号
40	28	(	开括号
41	29	)	闭括号
42	2A	*	星号
43	2B	+	加号
44	2C	,	逗号
45	2D	-	减号/破折号
46	2E	.	句号
47	2F	/	斜杠
48	30	0	数字0
49	31	1	数字1
50	32	2	数字2
51	33	3	数字3
52	34	4	数字4
53	35	5	数字5
54	36	6	数字6
55	37	7	数字7
56	38	8	数字8
57	39	9	数字9
58	3A	:	冒号
59	3B	;	分号
60	3C	<	小于
61	3D	=	等号
62	3E	>	大于
63	3F	?	问号
64	40	@	电子邮件符号
65	41	A	大写字母A　
66	42	B	大写字母B
67	43	C	大写字母C
68	44	D	大写字母D
69	45	E	大写字母E
70	46	F	大写字母F
71	47	G	大写字母G
72	48	H	大写字母H
73	49	I	大写字母I
74	4A	J	大写字母J
75	4B	K	大写字母K
76	4C	L	大写字母L
77	4D	M	大写字母M
78	4E	N	大写字母N
79	4F	O	大写字母O
80	50	P	大写字母P
81	51	Q	大写字母Q
82	52	R	大写字母R
83	53	S	大写字母S
84	54	T	大写字母T
85	55	U	大写字母U
86	56	V	大写字母V
87	57	W	大写字母W
88	58	X	大写字母X
89	59	Y	大写字母Y
90	5A	Z	大写字母Z
91	5B	[	开方括号
92	5C	\	反斜杠
93	5D	]	闭方括号
94	5E	^	脱字符
95	5F	_	下划线
96	60	`	开单引号
97	61	a	小写字母a　
98	62	b	小写字母b
99	63	c	小写字母c
100	64	d	小写字母d
101	65	e	小写字母e
102	66	f	小写字母f
103	67	g	小写字母g
104	68	h	小写字母h
105	69	i	小写字母i
106	6A	j	小写字母j
107	6B	k	小写字母k
108	6C	l	小写字母l
109	6D	m	小写字母m
110	6E	n	小写字母n
111	6F	o	小写字母o
112	70	p	小写字母p
113	71	q	小写字母q
114	72	r	小写字母r
115	73	s	小写字母s
116	74	t	小写字母t
117	75	u	小写字母u
118	76	v	小写字母v
119	77	w	小写字母w
120	78	x	小写字母x
121	79	y	小写字母y
122	7A	z	小写字母z
123	7B	{	开花括号
124	7C	|	垂线
125	7D	}	闭花括号
126	7E	~	波浪号
127	7F	DEL (delete)	删除"""
key_code = """
常量名称	十六位值	十位值	鼠标或按钮的值
VK_LBUTTON	1	1	鼠标左键钮
VK_RBUTTON	2	2	鼠标右键钮
VK_CANCEL	3	3	Control-break执行
VK_MBUTTON	4	4	鼠标中键钮
	05-07	05-07	未定义
VK_BACK	8	8	Backspace键
VK_TAB	9	9	Tab键
	0A-0B	10-11	未定义
VK_CLEAR	0C	12	Clear键
VK_RETURN	0D	13	Enter键
	0E-0F	14-15	未定义
VK_SHIFT	10	16	Shift键
VK_CONTROL	11	17	Ctrl键
VK_MENU	12	18	Alt键
VK_PAUSE	13	19	Pause键
VK_CAPITAL	14	20	Caps Lock键
	15-19	21-25	保留给Kanji系统使用
	1A	26	未定义
VK_ESCAPE	1B	27	Esc键
	1C-1F	28-31	保留给Kanji系统使用
VK_SPACE	20	32	SpaceBar键
VK_PRIOR	21	33	Page Up键
VK_NEXT	22	34	Page Down键
VK_END	23	35	End键
VK_HOME	24	36	Home键
VK_LEFT	25	37	Left Arrow键
VK_UP	26	38	Up Arrow键
VK_RIGHT	27	39	Right Arrow键
VK_DOWN	28	40	Down Arrow键
VK_SELECT	29	41	Select键
	2A	42	OEM自订使用
VK_EXECUTE	2B	43	Execute键
VK_SNAPSHOT  2C	44	Print Screen键
VK_INSERT	2D	45	Ins键
VK_DELETE	2E	46	Del键
VK_HELP	2F	47	Help键
VK_0	30	48	０键
VK_1	31	49	１键
VK_2	32	50	２键
VK_3	33	51	３键
VK_4	34	52	４键
VK_5	35	53	５键
VK_6	36	54	６键
VK_7	37	55	７键
VK_8	38	56	８键
VK_9	39	57	９键
	3A-40	58-64	未定义
VK_A	41	65	Ａ键
VK_B	42	66	Ｂ键
VK_C	43	67	Ｃ键
VK_D	44	68	Ｄ键
VK_E	45	69	Ｅ键
VK_F	46	70	Ｆ键
VK_G	47	71	Ｇ键
VK_H	48	72	Ｈ键
VK_I	49	73	Ｉ键
VK_J	4A	74	Ｊ键
VK_K	4B	75	Ｋ键
VK_L	4C	76	Ｌ键
VK_M	4D	77	Ｍ键
VK_N	4E	78	Ｎ键
VK_O	4F	79	Ｏ键
VK_P	50	80	Ｐ键
VK_Q	51	81	Ｑ键
VK_R	52	82	Ｒ键
VK_S	53	83	Ｓ键
VK_T	54	84	Ｔ键
VK_U	55	85	Ｕ键
VK_V	56	86	Ｖ键
VK_W	57	87	Ｗ键
VK_X	58	88	Ｘ键
VK_Y	59	89	Ｙ键
VK_Z	5A	90	Ｚ键
	5B-5F	91-95	未定义
VK_NUMPAD0	60	96	数字键０键
VK_NUMPAD1	61	97	数字键１键
VK_NUMPAD2	62	98	数字键２键
VK_NUMPAD3	63	99	数字键３键
VK_NUMPAD4	64	100	数字键４键
VK_NUMPAD5	65	101	数字键５键
VK_NUMPAD6	66	102	数字键６键
VK_NUMPAD7	67	103	数字键７键
VK_NUMPAD8	68	104	数字键８键
VK_NUMPAD9	69	105	数字键９键
VK_MULTIPLY  6A	106	＊键
VK_ADD	6B	107	＋键
VK_SEPARATOR  6C	108	Separator键
VK_SUBTRACT  6D	109	－键
VK_DECIMAL	6E	110	．键
VK_DIVIDE	6F	111	／键
VK_F1	70	112	F1键
VK_F2	71	113	F2键
VK_F3	72	114	F3键
VK_F4	73	115	F4键
VK_F5	74	116	F5键
VK_F6	75	117	F6键
VK_F7	76	118	F7键
VK_F8	77	119	F8键
VK_F9	78	120	F9键
VK_F10	79	121	F10键
VK_F11	7A	122	F11键
VK_F12	7B	123	F12键
VK_F13	7C	124	F13键
VK_F14	7D	125	F14键
VK_F15	7E	126	F15键
VK_F16	7F	127	F16键
VK_F17	80	128	F17键
VK_F18	81	129	F18键
VK_F19	82	130	F19键
VK_F20	83	131	F20键
VK_F21	84	132	F21键
VK_F22	85	133	F22键
VK_F23	86	134	F23键
VK_F24	87	135	F24键
	88-8F	136-143	未指定
VK_NUMLOCK	90	144	Num Lock键
VK_SCROLL	91	145	Scroll Lock键
	92-B9	146-185	未指定
	BA-C0	186-192	OEM自订
	C1-DA	193-218	未指定
	DB-E4	219-228	OEM自订
	E5	229	未指定
	E6	230	OEM自订
	E7-E8	231-232	未指定
	E9-F5	233-245	OEM自订
	F6-FE	246-254	未指定
"""
def onMouseEvent(event):
    # 监听鼠标事件
    print("MessageName:", event.MessageName)
    print("Message:", event.Message)
    print("Time:", event.Time)
    print("Window:", event.Window)
    print("WindowName:", event.WindowName)
    print("Position:", event.Position)
    print("Wheel:", event.Wheel)
    print("Injected:", event.Injected)
    print("---")
 
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True
 
def onKeyboardEvent(event):
    # 监听键盘事件
    print("MessageName:", event.MessageName)
    print("Message:", event.Message)
    print("Time:", event.Time)
    print("Window:", event.Window)
    print("WindowName:", event.WindowName)
    print("Ascii:", event.Ascii, chr(event.Ascii))
    print("Key:", event.Key)
    print("KeyID:", event.KeyID)
    print("ScanCode:", event.ScanCode)
    print("Extended:", event.Extended)
    print("Injected:", event.Injected)
    print("Alt", event.Alt)
    print("Transition", event.Transition)
    print("---")
 
    # 同鼠标事件监听函数的返回值
    return True
 
def log():
    # 创建一个“钩子”管理对象
    import pyHook
    import pythoncom
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()
if __name__ == "__main__":
    zk = zen_key()
    zk.press("r")
    
