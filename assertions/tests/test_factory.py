# -*- coding: utf8 -*-
from sys import version as SYS_VERSION
from unittest import TestCase
from mock import Mock, call
from assertions import factory

class cmp_assertionTest(TestCase):
    def setUp(self):
        self.compare = Mock()
        self.assertion = factory.cmp_assertion(self.compare)

    def test_it_build_a_function_that_call_succeed_if_comparison_is_true(self):
        self.compare_returns(True)
        self.assertion('a', 'b')

        self.compare.true.assert_called_once_with('a', 'b')
        self.compare.succeed.assert_called_once_with('a', 'b', '')

    def test_it_build_a_function_that_call_fail_if_comparison_is_false(self):
        self.compare_returns(False)
        self.assertion('a', 'b')

        self.compare.true.assert_called_once_with('a', 'b')
        self.compare.fail.assert_called_once_with('a', 'b', '')

    def test_can_define_and_override_default_message(self):
        self.compare_returns(True)
        expected_default = "default message"
        expected_overriden = "overriden message"
        self.assertion = factory.cmp_assertion(self.compare, expected_default)

        self.assertion('a', 'b', expected_overriden)
        self.assertion('a', 'b')

        expected = [call('a', 'b', expected_overriden), call('a', 'b', expected_default)]

        self.compare.succeed.assert_has_calls(expected)

    if SYS_VERSION > '3': # compile optimized not supported before
        def test_in_optimize_mode_it_returns_null_function(self):
            source_file = open(factory.__file__)
            source = source_file.read()
            source_file.close()
            result = compile(source, factory.__file__, mode='exec', optimize=1)
            exc_result = {}
            eval(result, globals(), exc_result)

            assertion = exc_result['cmp_assertion'](None)
            assert assertion('a', 'b') is None

    def compare_returns(self, boolean):
        config = {'true.return_value': boolean}
        self.compare.configure_mock(**config)


class compare_interfaceTest(TestCase):
    def test_it_must_have_callable_attr_true_succeed_and_fail(self):
        class compare(object):
            true = fail = succeed = lambda: None

        factory.cmp_assertion(compare)

    def test_if_it_has_not_true_callable_attr_it_raises_assertion_error(self):
        class compare_without_true(object):
            fail = succeed = lambda: None
        class compare_with_true_not_callable(compare_without_true):
            true = None

        with self.assertRaises(AssertionError):
            factory.cmp_assertion(compare_without_true())
        with self.assertRaises(AssertionError):
            factory.cmp_assertion(compare_with_true_not_callable())

    def test_if_it_has_not_succeed_callable_attr_it_raises_assertion_error(self):
        class compare_without_succeed(object):
            true = fail = lambda: None
        class compare_with_succeed_not_callable(compare_without_succeed):
            succeed = None

        with self.assertRaises(AssertionError):
            factory.cmp_assertion(compare_without_succeed())
        with self.assertRaises(AssertionError):
            factory.cmp_assertion(compare_with_succeed_not_callable())

    def test_if_it_has_not_fail_callable_attr_it_raises_assertion_error(self):
        class compare_without_fail(object):
            true = succeed = lambda: None
        class compare_with_fail_not_callable(compare_without_fail):
            fail = None

        with self.assertRaises(AssertionError):
            factory.cmp_assertion(compare_without_fail())
        with self.assertRaises(AssertionError):
            factory.cmp_assertion(compare_with_fail_not_callable())
