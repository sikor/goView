import random


def random_element(collection):
    return collection[random.randint(0, len(collection) - 1)]


def is_blank(string):
    return not string.strip()





