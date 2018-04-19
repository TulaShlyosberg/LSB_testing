

def extract_data(path):
    f_data = open(path, "rb")
    data = []
    for line in f_data.readlines():
        data += list(line)
    if data[-1] != 0:
        data.append(0)
    return data


def extract_byte(byte):
    byte1 = "" + bin(byte)[2:]
    while len(byte1) < 8:
        byte1 = '0' + byte1
    return byte1


def write_data(data, pic, code):
    ind = 0
    LAST_ZERO_BYTE = 254
    ans = []

    if (len(data) * 8 > len(pic) and code == 3) or (code == 4 and len(data) * 8 > int(len(pic) * 3 / 4)):
        print("Your data is too big.")
        exit(0)

    for byte in data:
        byte1 = extract_byte(byte)
        for bit in byte1:
            if ind % code == 0:
                x = pic[ind] & LAST_ZERO_BYTE if bit == '0' else pic[ind] | 1
            else:
                x = pic[ind]
            ans.append(x)
            ind += 1
    for elem in pic[ind:]:
        ans.append(elem)
    return ans


def extract_message(pic, code):
    res = list()
    res_byte = 1
    ind = 0
    while res_byte != 0:
        res_byte = 0
        for i in range(8):
            if ind % code == 0:
                res_byte = res_byte*2 + (pic[ind] & 1)
            ind += 1
        res.append(res_byte)
    return res
