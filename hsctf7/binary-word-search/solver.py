from PIL import Image

im = Image.open("BinaryWordSearch.png")

N = 1000

xs = []

for x in range(N):
    for y in range(N):
        (r, g, b) = im.getpixel((x, y))
        assert r == g and g == b and (r == 0 or r == 255)
        xs.append(r // 255)

pattern = "flag{"
M = len(pattern)


def search(suc):
    for i in range(N*N):
        ok = True
        k = i
        for j in range(M):
            ys = []
            for _ in range(8):
                if k < 0 or k >= N*N:
                    break
                ys.append(xs[k])
                k = suc(k)
            ok &= len(ys) == 8
            if ok:
                ok &= pattern[j] == chr(int("0b" + "".join(map(str, ys)), 2))
        if ok:
            k = i
            line = ""
            for j in range(30):
                ys = []
                for _ in range(8):
                    if k < 0 or k >= N*N:
                        break
                    ys.append(xs[k])
                    k = suc(k)
                if len(ys) != 8:
                    break
                c = int("0b" + "".join(map(str, ys)), 2)
                print("{}: {}".format(c, chr(c)))
                line += chr(c)
            print(line)
            print()


search(lambda x: x + 1)
search(lambda x: x - 1)
search(lambda x: x + N)
search(lambda x: x - N)
search(lambda x: x + (N + 1))
search(lambda x: x + (N - 1))
search(lambda x: x - (N + 1))
search(lambda x: x - (N - 1))
