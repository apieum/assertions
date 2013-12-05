# -*- coding: utf8 -*-

def cmp_assertion(compare, default_msg=''):
    assert is_compare(compare)

    def assertion(given, expected, msg=default_msg):
        if __debug__:
            if compare.true(given, expected):
                compare.succeed(given, expected, msg)
            else:
                compare.fail(given, expected, msg)
    return assertion

if __debug__:
    def is_compare(compare):
        return callable(getattr(compare, 'true', None)) \
            and callable(getattr(compare, 'succeed', None)) \
            and callable(getattr(compare, 'fail', None))
