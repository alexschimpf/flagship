# type: ignore

from unittest import TestCase

from app.constants import Operator
from app.api.routes.feature_flags.condition_checker import ConditionChecker


class TestConditionChecker(TestCase):
    def test_handle_string__equals_true(self) -> None:
        res = ConditionChecker._handle_string(context_value='blah', operator=Operator.EQUALS, condition_value='blah')
        self.assertTrue(res)

    def test_handle_string__equals_false(self) -> None:
        res = ConditionChecker._handle_string(context_value='blah', operator=Operator.EQUALS, condition_value='ahhh')
        self.assertFalse(res)

    def test_handle_string__not_equals_true(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='blah', operator=Operator.NOT_EQUALS, condition_value='ahhh'
        )
        self.assertTrue(res)

    def test_handle_string__not_equals_false(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='blah', operator=Operator.NOT_EQUALS, condition_value='blah'
        )
        self.assertFalse(res)

    def test_handle_string__in_list_true(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='blah', operator=Operator.IN_LIST, condition_value=['eh', 'blah']
        )
        self.assertTrue(res)

    def test_handle_string__in_list_false(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='blah', operator=Operator.IN_LIST, condition_value=['eh', 'ah']
        )
        self.assertFalse(res)

    def test_handle_string__not_in_list_true(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='blah', operator=Operator.NOT_IN_LIST, condition_value=['eh', 'ah']
        )
        self.assertTrue(res)

    def test_handle_string__not_in_list_false(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='blah', operator=Operator.NOT_IN_LIST, condition_value=['eh', 'blah']
        )
        self.assertFalse(res)

    def test_handle_string__matches_regex_true(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='1.2.3', operator=Operator.MATCHES_REGEX, condition_value=r'[1-9]\.[2-9]\.[0-9]*'
        )
        self.assertTrue(res)

    def test_handle_string__matches_regex_false(self) -> None:
        res = ConditionChecker._handle_string(
            context_value='1.2.3', operator=Operator.MATCHES_REGEX, condition_value=r'[1-9]\.[3-9]\.[0-9]*'
        )
        self.assertFalse(res)

    def test_handle_string__context_value_not_string(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_string(
                context_value=999, operator=Operator.EQUALS, condition_value='condition_value'
            )

    def test_handle_string__invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            ConditionChecker._handle_string(
                context_value='context_value', operator=None, condition_value='condition_value'
            )

    def test_handle_number__equals_true(self) -> None:
        res = ConditionChecker._handle_number(context_value=123.1, operator=Operator.EQUALS, condition_value=123.1)
        self.assertTrue(res)

    def test_handle_number__equals_false(self) -> None:
        res = ConditionChecker._handle_number(context_value=999.1, operator=Operator.EQUALS, condition_value=123.1)
        self.assertFalse(res)

    def test_handle_number__not_equals_true(self) -> None:
        res = ConditionChecker._handle_number(context_value=123.1, operator=Operator.NOT_EQUALS, condition_value=999.1)
        self.assertTrue(res)

    def test_handle_number__not_equals_false(self) -> None:
        res = ConditionChecker._handle_number(context_value=123.1, operator=Operator.NOT_EQUALS, condition_value=123.1)
        self.assertFalse(res)

    def test_handle_number__greater_than_true(self) -> None:
        res = ConditionChecker._handle_number(context_value=999.1, operator=Operator.GREATER_THAN, condition_value=1.1)
        self.assertTrue(res)

    def test_handle_number__greater_than_false(self) -> None:
        res = ConditionChecker._handle_number(context_value=1.1, operator=Operator.GREATER_THAN, condition_value=999.1)
        self.assertFalse(res)

    def test_handle_number__greater_than_or_equal_to_true(self) -> None:
        res = ConditionChecker._handle_number(
            context_value=123.1, operator=Operator.GREATER_THAN_OR_EQUAL_TO, condition_value=123.1
        )
        self.assertTrue(res)

    def test_handle_number__greater_than_or_equal_to_false(self) -> None:
        res = ConditionChecker._handle_number(
            context_value=1.1, operator=Operator.GREATER_THAN_OR_EQUAL_TO, condition_value=999.1
        )
        self.assertFalse(res)

    def test_handle_number__less_than_true(self) -> None:
        res = ConditionChecker._handle_number(context_value=1.1, operator=Operator.LESS_THAN, condition_value=999.1)
        self.assertTrue(res)

    def test_handle_number__less_than_false(self) -> None:
        res = ConditionChecker._handle_number(context_value=999.1, operator=Operator.LESS_THAN, condition_value=1.1)
        self.assertFalse(res)

    def test_handle_number__less_than_or_equal_to_true(self) -> None:
        res = ConditionChecker._handle_number(
            context_value=123.1, operator=Operator.LESS_THAN_OR_EQUAL_TO, condition_value=123.1
        )
        self.assertTrue(res)

    def test_handle_number__less_than_or_equal_to_false(self) -> None:
        res = ConditionChecker._handle_number(
            context_value=999.1, operator=Operator.LESS_THAN_OR_EQUAL_TO, condition_value=1.1
        )
        self.assertFalse(res)

    def test_handle_number__in_list_true(self) -> None:
        res = ConditionChecker._handle_number(context_value=1.1, operator=Operator.IN_LIST, condition_value=[2.1, 1.1])
        self.assertTrue(res)

    def test_handle_number__in_list_false(self) -> None:
        res = ConditionChecker._handle_number(context_value=1.1, operator=Operator.IN_LIST, condition_value=[2.1, 3.1])
        self.assertFalse(res)

    def test_handle_number__not_in_list_true(self) -> None:
        res = ConditionChecker._handle_number(
            context_value=1.1, operator=Operator.NOT_IN_LIST, condition_value=[2.1, 3.1]
        )
        self.assertTrue(res)

    def test_handle_number__not_in_list_false(self) -> None:
        res = ConditionChecker._handle_number(
            context_value=1.1, operator=Operator.NOT_IN_LIST, condition_value=[2.1, 1.1]
        )
        self.assertFalse(res)

    def test_handle_number__context_value_not_numeric(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_number(
                context_value='blah', operator=Operator.EQUALS, condition_value='condition_value'
            )

    def test_handle_number__invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            ConditionChecker._handle_number(context_value=123.1, operator=None, condition_value='condition_value')

    def test_handle_integer__equals_true(self) -> None:
        res = ConditionChecker._handle_integer(context_value=123, operator=Operator.EQUALS, condition_value=123)
        self.assertTrue(res)

    def test_handle_integer__equals_false(self) -> None:
        res = ConditionChecker._handle_integer(context_value=999, operator=Operator.EQUALS, condition_value=123)
        self.assertFalse(res)

    def test_handle_integer__not_equals_true(self) -> None:
        res = ConditionChecker._handle_integer(context_value=123, operator=Operator.NOT_EQUALS, condition_value=999)
        self.assertTrue(res)

    def test_handle_integer__not_equals_false(self) -> None:
        res = ConditionChecker._handle_integer(context_value=123, operator=Operator.NOT_EQUALS, condition_value=123)
        self.assertFalse(res)

    def test_handle_integer__greater_than_true(self) -> None:
        res = ConditionChecker._handle_integer(context_value=999, operator=Operator.GREATER_THAN, condition_value=1)
        self.assertTrue(res)

    def test_handle_integer__greater_than_false(self) -> None:
        res = ConditionChecker._handle_integer(context_value=1, operator=Operator.GREATER_THAN, condition_value=999)
        self.assertFalse(res)

    def test_handle_integer__greater_than_or_equal_to_true(self) -> None:
        res = ConditionChecker._handle_integer(
            context_value=123, operator=Operator.GREATER_THAN_OR_EQUAL_TO, condition_value=123
        )
        self.assertTrue(res)

    def test_handle_integer__greater_than_or_equal_to_false(self) -> None:
        res = ConditionChecker._handle_integer(
            context_value=1, operator=Operator.GREATER_THAN_OR_EQUAL_TO, condition_value=999
        )
        self.assertFalse(res)

    def test_handle_integer__less_than_true(self) -> None:
        res = ConditionChecker._handle_integer(context_value=1, operator=Operator.LESS_THAN, condition_value=999)
        self.assertTrue(res)

    def test_handle_integer__less_than_false(self) -> None:
        res = ConditionChecker._handle_integer(context_value=999, operator=Operator.LESS_THAN, condition_value=1)
        self.assertFalse(res)

    def test_handle_integer__less_than_or_equal_to_true(self) -> None:
        res = ConditionChecker._handle_integer(
            context_value=123, operator=Operator.LESS_THAN_OR_EQUAL_TO, condition_value=123
        )
        self.assertTrue(res)

    def test_handle_integer__less_than_or_equal_to_false(self) -> None:
        res = ConditionChecker._handle_integer(
            context_value=999, operator=Operator.LESS_THAN_OR_EQUAL_TO, condition_value=1
        )
        self.assertFalse(res)

    def test_handle_integer__in_list_true(self) -> None:
        res = ConditionChecker._handle_integer(context_value=1, operator=Operator.IN_LIST, condition_value=[2, 1])
        self.assertTrue(res)

    def test_handle_integer__in_list_false(self) -> None:
        res = ConditionChecker._handle_integer(context_value=1, operator=Operator.IN_LIST, condition_value=[2, 3])
        self.assertFalse(res)

    def test_handle_integer__not_in_list_true(self) -> None:
        res = ConditionChecker._handle_integer(context_value=1, operator=Operator.NOT_IN_LIST, condition_value=[2, 3])
        self.assertTrue(res)

    def test_handle_integer__not_in_list_false(self) -> None:
        res = ConditionChecker._handle_integer(context_value=1, operator=Operator.NOT_IN_LIST, condition_value=[2, 1])
        self.assertFalse(res)

    def test_handle_integer__context_value_not_integer(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_integer(
                context_value=1.23, operator=Operator.EQUALS, condition_value='condition_value'
            )

    def test_handle_integer__invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            ConditionChecker._handle_integer(context_value=123, operator=None, condition_value='condition_value')

    def test_handle_enum__context_value_is_invalid_type(self) -> None:
        for context_value in ({}, []):
            with self.subTest(), self.assertRaises(TypeError):
                ConditionChecker._handle_enum(
                    context_value=context_value, operator=None, condition_value='condition_value'
                )

    def test_handle_enum__invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            ConditionChecker._handle_enum(context_value=123, operator=None, condition_value='condition_value')

    def test_handle_enum__equals_true(self) -> None:
        res = ConditionChecker._handle_enum(context_value=123, operator=Operator.EQUALS, condition_value=123)
        self.assertTrue(res)

    def test_handle_enum__equals_false(self) -> None:
        res = ConditionChecker._handle_enum(context_value=123, operator=Operator.EQUALS, condition_value=999)
        self.assertFalse(res)

    def test_handle_enum__not_equals_true(self) -> None:
        res = ConditionChecker._handle_enum(context_value=123, operator=Operator.NOT_EQUALS, condition_value=999)
        self.assertTrue(res)

    def test_handle_enum__not_equals_false(self) -> None:
        res = ConditionChecker._handle_enum(context_value=123, operator=Operator.NOT_EQUALS, condition_value=123)
        self.assertFalse(res)

    def test_handle_enum__in_list_true(self) -> None:
        res = ConditionChecker._handle_enum(context_value=123, operator=Operator.IN_LIST, condition_value=[123, 345])
        self.assertTrue(res)

    def test_handle_enum__in_list_false(self) -> None:
        res = ConditionChecker._handle_enum(context_value=123, operator=Operator.IN_LIST, condition_value=[345, 999])
        self.assertFalse(res)

    def test_handle_enum__not_in_list_true(self) -> None:
        res = ConditionChecker._handle_enum(
            context_value=123, operator=Operator.NOT_IN_LIST, condition_value=[345, 999]
        )
        self.assertTrue(res)

    def test_handle_enum__not_in_list_false(self) -> None:
        res = ConditionChecker._handle_enum(
            context_value=123, operator=Operator.NOT_IN_LIST, condition_value=[123, 345]
        )
        self.assertFalse(res)

    def test_handle_version__true(self):
        for context_value, operator, condition_value in (
            ('3.2.1', Operator.EQUALS, '3.2.1'),
            ('3.2', Operator.EQUALS, '3.2.0'),
            ('3.2.0', Operator.EQUALS, '3.2'),
            ('3.2.1', Operator.NOT_EQUALS, '3.2.2'),
            ('3.2.2', Operator.GREATER_THAN, '3.2.1'),
            ('3.2.1', Operator.GREATER_THAN_OR_EQUAL_TO, '3.2.1'),
            ('3.2.1', Operator.LESS_THAN, '3.2.2'),
            ('3.2.1', Operator.LESS_THAN_OR_EQUAL_TO, '3.2.1'),
        ):
            with self.subTest():
                res = ConditionChecker._handle_version(
                    context_value=context_value, operator=operator, condition_value=condition_value
                )
                self.assertTrue(res)

    def test_handle_version__false(self):
        for context_value, operator, condition_value in (
            ('3.2.1', Operator.NOT_EQUALS, '3.2.1'),
            ('3.2', Operator.NOT_EQUALS, '3.2.0'),
            ('3.2.0', Operator.NOT_EQUALS, '3.2'),
            ('3.2.1', Operator.EQUALS, '3.2.2'),
            ('3.2.2', Operator.LESS_THAN, '3.2.1'),
            ('3.2.1', Operator.LESS_THAN, '3.2.1'),
            ('3.2', Operator.LESS_THAN_OR_EQUAL_TO, '2'),
            ('3.2.1', Operator.GREATER_THAN, '3.2.2'),
            ('3.2.1', Operator.GREATER_THAN, '3.2.1'),
            ('2', Operator.GREATER_THAN_OR_EQUAL_TO, '3.2'),
        ):
            with self.subTest():
                res = ConditionChecker._handle_version(
                    context_value=context_value, operator=operator, condition_value=condition_value
                )
                self.assertFalse(res)

    def test_handle_list__contains_true(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.CONTAINS, condition_value=2, list_type=int
        )
        self.assertTrue(res)

    def test_handle_list__contains_false(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.CONTAINS, condition_value=999, list_type=int
        )
        self.assertFalse(res)

    def test_handle_list__not_contains_true(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.NOT_CONTAINS, condition_value=999, list_type=int
        )
        self.assertTrue(res)

    def test_handle_list__not_contains_false(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.NOT_CONTAINS, condition_value=2, list_type=int
        )
        self.assertFalse(res)

    def test_handle_list__intersects_true(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.INTERSECTS, condition_value=[3, 4], list_type=int
        )
        self.assertTrue(res)

    def test_handle_list__intersects_false(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.INTERSECTS, condition_value=[4, 5], list_type=int
        )
        self.assertFalse(res)

    def test_handle_list__not_intersects_true(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.NOT_INTERSECTS, condition_value=[4, 5], list_type=int
        )
        self.assertTrue(res)

    def test_handle_list__not_intersects_false(self) -> None:
        res = ConditionChecker._handle_list(
            context_value=[1, 2, 3], operator=Operator.NOT_INTERSECTS, condition_value=[3, 4], list_type=int
        )
        self.assertFalse(res)

    def test_handle_list__invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            ConditionChecker._handle_list(
                context_value=[1, 2], operator=None, condition_value='condition_value', list_type=int
            )

    def test_handle_list__context_value_not_string_list(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_list(
                context_value=[1, 2], operator=None, condition_value='condition_value', list_type=str
            )

    def test_handle_list__context_value_not_integer_list(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_list(
                context_value=['abc', 'def'], operator=None, condition_value='condition_value', list_type=int
            )

    def test_handle_list__context_value_not_string_integer_or_float_list(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_list(
                context_value=[[]], operator=None, condition_value='condition_value', list_type=(str, int, float)
            )

    def test_handle_boolean__equals_true(self) -> None:
        res = ConditionChecker._handle_boolean(context_value=True, operator=Operator.EQUALS, condition_value=True)
        self.assertTrue(res)

    def test_handle_boolean__equals_false(self) -> None:
        res = ConditionChecker._handle_boolean(context_value=True, operator=Operator.EQUALS, condition_value=False)
        self.assertFalse(res)

    def test_handle_boolean__not_equals_true(self) -> None:
        res = ConditionChecker._handle_boolean(context_value=True, operator=Operator.NOT_EQUALS, condition_value=False)
        self.assertTrue(res)

    def test_handle_boolean__not_equals_false(self) -> None:
        res = ConditionChecker._handle_boolean(context_value=True, operator=Operator.NOT_EQUALS, condition_value=True)
        self.assertFalse(res)

    def test_handle_boolean__context_value_not_boolean(self) -> None:
        with self.assertRaises(TypeError):
            ConditionChecker._handle_boolean(context_value='blah', operator=Operator.EQUALS, condition_value=True)

    def test_handle_boolean__invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            ConditionChecker._handle_integer(context_value=True, operator=None, condition_value=True)
