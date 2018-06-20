# vim:fileencoding=utf-8
# author: SaiChrla

# Creats an array of bytes from a file for testing GCO and TDACS communication

def get_frames(file_name='Thermal_Data_Transfer_Sample.txt'):
    """Gets the gc frames from the text file"""
    with open(file_name, 'r', encoding='utf-8') as f:
        sl = f.readlines()
    sl = [line.rstrip('\n') for line in sl if line[0] == '\x02']
    sb = [bytes(line, 'cp1252') for line in sl]
    return sb


if __name__ == "__main__":
    import pprint
    # file_name = 'Thermal_Data_Transfer_Sample.txt' kwarg
    pprint.pprint(get_frames())

