# vim:fileencoding=utf-8
# author: SaiChrla


import threading
import client_branch as c

host_list = []

for address in host_list:
    client_branch_thread.append(threading.Thread(target=c.client_branch,
            args=address))
for thread in client_branch_thread:
    thread.start()

