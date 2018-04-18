def binarization(d):
    ans = []
    for elem in d:
        x = bin(ord(elem))[2:]
        while len(x) < 8:
            x = '0' + x
        ans += list(x)
    return ans


f_data = open("data.txt", "r")
f_pic = open("pic.txt", "r")

data = []
for line in f_data.readlines():
    data += list(line)
if data[-1] != '\0':
    data.append('\0')
bin_data = binarization(data)

pic = f_pic.readline()
ind = 0
LAST_ZERO_BYTE = ((((1 << 9) - 1) >> 1) << 1)
fout = open("stegopic.txt", "w")
for bit in bin_data:
    pic[ind] = pic[ind] & LAST_ZERO_BYTE if bit == '0' else pic[ind] = pic[ind] | 1
    ind += 1
    print(pic[ind], end='', file=fout)
print(''.join(pic[ind:]))
fout.close()
