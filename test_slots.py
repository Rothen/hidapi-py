import timeit
from statistics import mean

class Foo(object):
    __slots__ = 'foo',


class Bar(object):
    pass


slotted = Foo()
not_slotted = Bar()


def get_set_delete_fn(obj):
    def get_set_delete():
        obj.foo = 'foo'
        obj.foo
        del obj.foo
    return get_set_delete


res_slotted = mean(timeit.repeat(get_set_delete_fn(slotted)))
res_unslotted = mean(timeit.repeat(get_set_delete_fn(slotted)))

print(res_slotted)
print(res_unslotted)

print(res_unslotted / res_slotted)