import os
import time
import sys
import subprocess

home = os.path.expanduser('~')
os.chdir(home)
flag = False

std_kwargs = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
}

try:
    print('starting server')
    process = subprocess.Popen('wk-viewer', shell=True, **std_kwargs)
    url = "localhost:5000"

    #wait for file-xfer-legacy to come up
    time.sleep(1.5)

    c = subprocess.Popen(
        ("curl -o /dev/null --silent --head "
            "--write-out '%{http_code}\n' " + url),
        shell=True, stdout=subprocess.PIPE)
    status = c.communicate()[0].strip()
    print('the status: %s' % status)

    if status == '200':
        print('a-o-k')
        flag = True
    else:
        flag = False

finally:
    process.terminate()

#test failed exit!
if not flag:
    print('Failed test!')
    sys.exit(9)
