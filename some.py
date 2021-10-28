import random


def gen_rand_no():
    used_numbers_lst = []
    for counter in range(5000):
        rand = random.randint(1, 5500)
        if rand not in used_numbers_lst:
            return rand
        used_numbers_lst.append(rand)


print('Some: 3', end="")
