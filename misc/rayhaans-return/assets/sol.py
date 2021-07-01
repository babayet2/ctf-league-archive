pieces = {}

for line in open("pieces"):
    line = line.strip()

    idx, data = line.split("\t")
    data = bytes.fromhex(data)

    try:
        pieces[idx] += data
    except KeyError:
        pieces[idx] = data

pieces = sorted([(p[0], p[1]) for p in pieces.items()])


x = b"".join([p[1] for p in pieces])
open("torrent.out", "wb").write(x)
