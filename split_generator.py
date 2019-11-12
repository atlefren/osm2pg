# -*- coding: utf-8 -*-


def split_generator(gen, elements_pr_generator):
    is_running = True

    def generator(gen):
        nonlocal is_running
        c = 0
        while c < elements_pr_generator:
            try:
                n = next(gen)
                yield n
            except StopIteration as e:
                is_running = False
                raise e
            c += 1

    c = 0
    while is_running:
        if c % elements_pr_generator == 0:
            yield generator(gen)
        c += 1
