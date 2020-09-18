"""Telegram Bot"""
# pylint: disable=no-member invalid-name
from socket import socket, gethostbyname
from ssl import SSLContext, SSLZeroReturnError, SSLError
from json import loads, dumps
from time import sleep
from threading import Thread


class Message():
    """Message class"""

    def __init__(self, event):
        if "ok" in event:
            self.ok = event["ok"]
        else:
            self.ok = True
        if "update_id" in event:
            self.update_id = event["update_id"]
            event = event["message"]

        if "from" in event:
            self.user = self.From(event["from"])
            del event["from"]
        if "chat" in event:
            self.chat = self.Chat(event["chat"])
            del event["chat"]

        for i in event:
            if isinstance(event[i], list):
                if len(event[i]) == 1:
                    event[i] = event[i][0]
                for j in event[i]:
                    # To test, dynamic class creation
                    # if isinstance(j, dict):
                    #    for k in j:
                    #        self.__dict__[k] = j[k]
                    #    new_class = type(i, (), {
                    #        "__init__": lambda self: for l in j: self.__dict__[l] = j[l]
                    #    })
                    if isinstance(event[i][j], dict):
                        for k in event[i][j]:
                            self.__dict__[i][j][k] = event[i][j][k]
                    else:
                        self.__dict__[j] = event[i][j]  # [i][j] ?
            else:
                self.__dict__[i] = event[i]

    class From():
        """from dictionary value"""

        def __init__(self, event):
            for i in event:
                self.__dict__[i] = event[i]

    class Chat():
        """chat dictionary value"""

        def __init__(self, event):
            for i in event:
                self.__dict__[i] = event[i]


class TBot():
    """Main Class"""

    def __init__(self, TOKEN: str):
        self.__url = gethostbyname("api.telegram.org")
        self.__token = TOKEN
        self.__commands = {}
        self.__offset = 0
        self.update_frequence = 1  # seconds
        self.username: str
        self.__process_func = [] #only 1? : function
        self.__sock = None
        self.__sock = self.__connect(self.__sock) #mhhhhhhh
        self.__solve_me()

    def __connect(self, sock):
        if hasattr(sock, "closed"):
            if not sock.closed:
                sock.close()
        sock = socket(2, 1)
        sock.connect((self.__url, 443))
        sock = SSLContext().wrap_socket(sock)
        return sock

    def __solve_me(self):
        if (response:= self.__get("getMe")):
            self.username = '@' + response.username

    def __get(self, method, arguments=None):
        request = f"GET /bot{self.__token}/{method}"
        multiple = False
        if arguments:
            for i in arguments:
                if multiple:
                    request += '&'
                else:
                    request += '?'
                    multiple = True
                request += i + '=' + str(arguments[i])
        request += f" HTTP/1.1\nHost: {self.__url}\n\n"
        self.__sock.send(request.encode())
        try:
            response = loads(self.__sock.recv(
                65535 * 20).decode().split("\r\n\r\n", 1)[1])
            if response["ok"]:
                retval = []
                response = response["result"]
                if isinstance(response, list):
                    for i in response:
                        retval.append(Message(i))
                    return retval
                return Message(response)
            # return False
        except IndexError:
            # return False
            pass
        except SSLError:
            self.__sock = self.__connect(self.__sock)

    def _update(self):
        if (response:= self.__get("getUpdates", {"offset": self.__offset})):
            self.__offset = response[len(response) - 1].update_id + 1
            return response
        return None

    def _check(self):
        response = self._update()
        if not response:
            return
        for i in response:
            if hasattr(i, "type"):
                if i.type == "bot_command":
                    match = False
                    if i.type == "supergroup":
                        i.text = i.text.replace(
                            self.username, '')
                    for j in self.__commands:
                        if j == i.text:
                            Thread(target=self.__commands[j](i)).start()
                            match = True
                            break
                    if not match and '*' in self.__commands:
                        self.__commands['*'](i)
            for k in self.__process_func:
                Thread(target=k, args=[i, ]).start()

    def command(self, *args):
        """Add a command handler"""
        def wrapper(func):
            self.__commands[args[0]] = func
            return func
        return wrapper

    def process(self, func):
        """
        Add a process handler.

        Functions added here will be called every time there is an update.
        """
        self.__process_func.append(func)

    def run(self):
        """Start the bot"""
        while 1:
            try:
                self._check()
            except (ConnectionAbortedError, SSLZeroReturnError):#, SSLError):
                self.__sock = self.__connect(self.__sock)
            sleep(self.update_frequence)

    def send_image_from_url(self, event, url):
        """Send an image to an user"""
        return self.__get("sendPhoto",
                          {"chat_id": event.chat_id, "photo": url}).ok

    def send(self, event, message, *args):
        """Send a message"""
        message = {
            "chat_id": event.chat.id,
            "text": message.replace("\n", "%0A")
        }  # Use Message()
        for i in args:
            message[i[0]] = i[1]
        return self.__get("sendMessage", message)

    def send_id(self, chat_id, message):
        """Send a message to an id"""
        message = {
            "chat_id": chat_id,
            "text": message.replace("\n", "%0A")
        }  # Use Message()
        return self.__get("sendMessage", message)

    def get_chat(self, event):
        """Send chat informations"""
        return self.__get("getChat", {"chat_id": event.chat.id})


class Scheduler():
    """Schedule function call"""

    def __init__(self):
        self.__funcs = []

    def schedule(self, func, time, repeat=True, call=False, asynchronous=True):  # args=None
        """Schedule a new function call"""
        self.__funcs.append(func)
        if call:
            if asynchronous:
                Thread(target=func).start()
            else:
                func()
        if asynchronous:
            Thread(target=self.__scheduled, args=[func, time, repeat]).start()
        else:
            self.__scheduled(func, time, repeat)

    def remove(self, func):
        """Remove a scheduled function call"""
        del self.__funcs[func]

    def __scheduled(self, func, time, repeat):
        while 1:
            sleep(time)
            if func in self.__funcs and repeat:
                Thread(target=func).start()
            else:
                break


def keyboard(keys, temporary=False):
    """
    Return a telegram keyboard from a string array.
    keys=[[Top Items], [Middle Items], [Bottom Items]]
    """
    items = [item for item in keys]
    reply_markup = {"keyboard": items}
    if temporary:
        reply_markup["one_time_keyboard"] = True
    return ["reply_markup", dumps(reply_markup)]
