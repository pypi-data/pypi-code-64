# -*- coding: utf-8 -*-

import socket
import select
SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900
SERVICE_NAME = 'zen_service'
SSDP_HEADER = '''M-SEARCH * HTTP/1.1
HOST: %s:%d
MAN: "ssdp:discover"
MX: 2
ST: ssdp:all
''' % (SSDP_ADDR, SSDP_PORT)
"""
各HTTP协议头的含义简介：

HOST：设置为协议保留多播地址和端口，必须是：239.255.255.250:1900（IPv4）或FF0x::C(IPv6)

MAN：设置协议查询的类型，必须是：ssdp:discover

MX：设置设备响应最长等待时间，设备响应在0和这个值之间随机选择响应延迟的值。这样可以为控制点响应平衡网络负载。

ST：设置服务查询的目标，它必须是下面的类型：

　　ssdp:all 搜索所有设备和服务 
　　upnp:rootdevice 仅搜索网络中的根设备 
　　uuid:device-UUID 查询UUID标识的设备 
　　urn:schemas-upnp-org:device:device-Type:version 查询device-Type字段指定的设备类型，设备类型和版本由UPNP组织定义。 
　　urn:schemas-upnp-org:service:service-Type:version 查询service-Type字段指定的服务类型，服务类型和版本由UPNP组织定义。"""
class Connection():
    def __init__(self, s, data, addr):
        self.__s = s
        self.__data = data
        self.__addr = addr
        self.is_find_service = False

    def handle_request(self):
        if self.__data.startswith('M-SEARCH * HTTP/1.1\r\n'):
            self.__handle_search()
        elif self.__data.startswith('HTTP/1.1 200 OK\r\n'):
            self.__handle_ok()

    def __handle_search(self):
        props = self.__parse_props(['HOST', 'MAN', 'ST', 'MX'])
        if not props:
            return

        if props['HOST'] != '%s:%d' % (SSDP_ADDR, SSDP_PORT) \
                or props['MAN'] != '"ssdp:discover"' \
                or props['ST'] != 'ssdp:all':
            return
        print 'ADDR: %s' % str(self.__addr)
        print 'RECV: %s' % str(self.__data)
        
        response = 'HTTP/1.1 200 OK\r\nST: %s\r\n\r\n' % SERVICE_NAME
        self.__s.sendto(response, self.__addr)

    def __handle_ok(self):
        props = self.__parse_props(['ST'])
        if not props:
            return

        if props['ST'] != SERVICE_NAME:
            return
        print 'ADDR: %s' % str(self.__addr)
        print 'RECV: %s' % str(self.__data)
        self.is_find_service = True

    def __parse_props(self, target_keys):
        lines = self.__data.split('\r\n')

        props = {}
        for i in range(1, len(lines)):
            if not lines[i]:
                continue

            index = lines[i].find(':')
            if index == -1:
                return None

            props[lines[i][:index]] = lines[i][index + 1:].strip()

        if not set(target_keys).issubset(set(props.keys())):
            return None

        return props

class SSDPServer():
    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        local_ip = socket.gethostbyname(socket.gethostname())
        any_ip = '0.0.0.0'

        # 绑定到任意地址和SSDP组播端口上
        self.__s.bind((any_ip, SSDP_PORT))

        # INFO: 使用默认值
        # self.__s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
        # self.__s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
        # self.__s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,
        #                     socket.inet_aton(intf) + socket.inet_aton('0.0.0.0'))
        # INFO: 添加到多播组
        self.__s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                            socket.inet_aton(SSDP_ADDR) + socket.inet_aton(local_ip))
        self.local_ip = local_ip

    def start(self):
        while True:
            data, addr = self.__s.recvfrom(2048)
            conn = Connection(self.__s, data, addr)
            conn.handle_request()
        self.__s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                            socket.inet_aton(SSDP_ADDR) + socket.inet_aton(self.local_ip))
        self.__s.close()


class SSDPClient():
    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # INFO: 若绑定，服务端收到的是固定的地址和端口号
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        local_ip = socket.gethostbyname(socket.gethostname())
        self.__s.bind((local_ip, 50000))

    def start(self):
        self.__send_search()
        while True:
            reads, _, _ = select.select([self.__s], [], [], 5)
            if reads:
                data, addr = self.__s.recvfrom(2048)
                conn = Connection(self.__s, data, addr)
                conn.handle_request()
                if conn.is_find_service:
                    break
            else:  # timeout
                self.__send_search()
        self.__s.close()

    def __send_search(self):
        # print "Sending M-SEARCH..."
        # INFO: 发送到SSDP组播地址上
        self.__s.sendto(SSDP_HEADER, (SSDP_ADDR, SSDP_PORT))
if __name__ == '__main__':
    port = SSDPServer()
    port.start()
if __name__ == '__main__':
    port = SSDPClient()
    port.start()
