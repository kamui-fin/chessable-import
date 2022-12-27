import sys

def die(msg):
    print(msg, file=sys.stderr)
    exit(-1)

def chunks(lst, n):
    res = []
    for i in range(0, len(lst), n):
        res.append(lst[i:i + n])
    return res

def trim_name(name, k = 55, with_chunk = 0):
    name = ' '.join(name.replace("Chapter ", "").split())
    if len(name) > k and with_chunk > 0:
        return name[:k - with_chunk] + name[-with_chunk:]
    return name[:k]

def test_trim():
    assert trim_name("aaaaaabb", 5, 2) == "aaabb"
    assert trim_name("aaaaaa", 3, 0) == "aaa"
    assert trim_name("a", 1, 0)  == "a"
    assert trim_name("aaaab", 5, 1) == "aaaab"
    assert trim_name("Chapter 1") == "1"

