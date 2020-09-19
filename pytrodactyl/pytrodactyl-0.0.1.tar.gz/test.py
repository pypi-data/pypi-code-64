from pytrodactyl import Application
import time

app = Application(url="https://panel.fatcat.bike", api_key="Ni9Xd7Yt26A2yxtiMjHmC1rYdMKHEyLfc57q8p6wtSKl20RS")

print(app.show_all_servers())
