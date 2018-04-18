def extract_data():
    f_data = open("data.txt", "r")
    data = []
    for line in f_data.readlines():
        data += list(line)
    if data[-1] != '\0':
        data.append('\0')
    return data


def extract_byte(byte):
    byte1 = "" + byte[2:]
    while len(byte1) < 8:
        byte1 = '0' + byte1
    return byte1


def write_data(data, pic):
    ind = 0
    LAST_ZERO_BYTE = ((((1 << 9) - 1) >> 1) << 1)
    fout = open("stegopic.txt", "w")
    for byte in data:
        byte1 = extract_byte(byte)
        for bit in byte1:
            pic[ind] = chr(ord(pic[ind]) & LAST_ZERO_BYTE) if bit == '0' else chr(ord(pic[ind]) | 1)
            ind += 1
            print(pic[ind], end='', file=fout)
    print(''.join(pic[ind:]))
    fout.close()


def read_from_file():
    f_pic = open("pic.txt", "r")
    pic = f_pic.readline()
    return pic


def read_from_list(piclist):
    return ''.join(list(map(chr, piclist)))
