def a(s):
    l = [0]
    o = l * len(s)
    for i, c in enumerate(s):
        o[i] = c*2 - 60

    return o


def b(s, t):
    for x, y in zip(s, t):
        yield x + y - 50


def c(s):
    return [x + 5 for x in s] 


def e(s):
    s = [ord(c) for c in s]
    a_s = a(s)
    c_s = c(s)

    o = [(x^5) - 30 for x in b(a_s, c_s)]
    return bytes(o)


if __name__ == '__main__':
    s = input("guess?")
    o = b'\xae\xc0\xa1\xab\xef\x15\xd8\xca\x18\xc6\xab\x17\x93\xa8\x11\xd7\x18\x15\xd7\x17\xbd\x9a\xc0\xe9\x93\x11\xa7\x04\xa1\x1c\x1c\xed'
    
    if e(s) == o:
        print("Correct!")
    else:
        print("Wrong...")
        
