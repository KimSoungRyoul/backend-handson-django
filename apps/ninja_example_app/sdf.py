def add_num(n1, n2):

    try:
        return n1 + n2
    except TypeError:
        return int(n1) + int(n2)


if __name__ == "__main__":
    print(add_num(1, 2))  # 성공
    print(add_num(1, "2"))  # 성공
    print(add_num("1", 2))  # 성공
