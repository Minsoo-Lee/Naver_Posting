def test(i):
    i[0] += 1

def main():
    i = [0]
    print(i)
    test(i)
    print(i)

main()