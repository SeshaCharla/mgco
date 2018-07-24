# vim:fileencoding=utf-8
# author=SaiChrla


import logging


def log(msg, addr, level=0):
    """ Logs the message in to a file named after addr with set level"""
    # log levels
    # 0 - DEBUG
    # 1 - INFO
    # 2 - Warning
    # 3 - ERROR
    # 4 - WARNING

    fname = '{}_{}.log'.format(addr[0], str(addr[1]))
    logging.basicConfig(filename=fname, filemode='a', level=logging.DEBUG,
                    format='%(asctime)s ; %(levelname)s ; %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
    if level==0:
        logging.debug(msg)
    elif level==1:
        logging.info(msg)
    elif level==2:
        logging.warning(msg)
    elif level==3:
        logging.error(msg)
    elif level==4:
        logging.warning(msg)
    else:
        logging.debug(msg)
        logging.debug('The level set is not there, it should be in [0,4]')

