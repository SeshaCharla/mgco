# vim:fileencoding=utf-8
# SaiChrla

def get_config():
    """get the server addresses and no. of parameters from GC.conf"""
    with open('GC.conf') as f:
        s = f.readlines()
        addrs = []
        nparms = []
        st_list = []
        for line in s:
            if line[0] != '#':
                line.lstrip('\n')
                d = line.split(',')
                addr = (d[0], int(d[1]))
                nparm = int(d[2])
                st = int(d[3])
                addrs.append(addr)
                nparms.append(nparm)
                st_list.append(st)
        n = len(nparms)
        return n, addrs, nparms, st_list

def pipeline_config():
    """get the pipeline server addresses sleep time from pipeline.conf"""
    with open('pipeline.conf') as f:
        s = f.readlines()
        for line in s:
            if line[0] != '#':
                line.lstrip('\n')
                d = line.split(',')
                addr = (d[0], int(d[1]))
                sleeptime = int(d[2])
        return addr, sleeptime





if __name__ == "__main__":
    print(get_config())
    print(pipeline_config())

