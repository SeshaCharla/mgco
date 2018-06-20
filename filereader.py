# vim:fileencoding=utf-8
# author: SaiChrla


def readfile(host, port):
    """ Reads the data file corresponding to the server"""
    file_name = '{}_{}.dat'.format(host, str(port))
    with open(file_name, 'r', encoding='cp1252') as f:
        frame = f.read()
    return frame



