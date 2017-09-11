import timeit


def while_one():
    i = 0
    while 1:
        i += 1
        if i == 10000000:
            break


def while_true():
    i = 0
    while True:
        i += 1
        if i == 10000000:
            break


if __name__ == "__main__":
    w1 = timeit.timeit(while_one, "from __main__ import while_one", number=3)
    wt = timeit.timeit(while_true, "from __main__ import while_true", number=3)
    print("while one: %s\n while_true: %s" % (w1, wt))