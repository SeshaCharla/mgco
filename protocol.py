# vim:fileencoding=utf-8
# AUthor: SaiChrla


""" This file has the necessary functions for readign and wrinting data in GCO
protocol. cp1252 encoding is used as '\xbb' and '\xcc' are represented by
corresponding hex nos. unlike utf-8 where is split in to 2 nos. """


# Frame Headers
STX = bytes('\x02', 'cp1252')
ETX = bytes('\x03', 'cp1252')
DATA_FRAME = bytes('\xbb', 'cp1252')
DB_FRAME = bytes('\xcc', 'cp1252')
INVALID = bytes('\x00', 'cp1252')


#Test local address
TEST_HOST = '127.0.0.1'
TEST_PORT = '4040'
TEST_ADDR = (TEST_HOST, TEST_PORT)

# Buffer Size
BUF_SIZ = 4096  # 4 MB
