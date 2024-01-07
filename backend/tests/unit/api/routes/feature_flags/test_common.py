import unittest
from typing import Any

from app.api.exceptions import exceptions
from app.api.routes.feature_flags.controllers import common
from app.api.routes.feature_flags.schemas import FeatureFlagCondition
from app.constants import Operator, ContextValueType


class TestFeatureFlagsCommon(unittest.TestCase):

    def test_validate_and_group__pass(self) -> None:
        common._validate_and_group(and_group=[
            FeatureFlagCondition(
                context_key='blah',
                operator=Operator.EQUALS,
                value='1'
            ),
            FeatureFlagCondition(
                context_key='blah2',
                operator=Operator.NOT_EQUALS,
                value='2'
            )
        ])

    def test_validate_and_group__fail(self) -> None:
        with self.assertRaises(exceptions.SameContextFieldKeysInAndGroup):
            common._validate_and_group(and_group=[
                FeatureFlagCondition(
                    context_key='blah',
                    operator=Operator.EQUALS,
                    value='1'
                ),
                FeatureFlagCondition(
                    context_key='blah',
                    operator=Operator.NOT_EQUALS,
                    value='2'
                )
            ])

    def test_validate_context_field_and_operator__pass(self) -> None:
        params: Any = [
            (ContextValueType.STRING, Operator.EQUALS),
            (ContextValueType.STRING, Operator.NOT_EQUALS),
            (ContextValueType.STRING, Operator.MATCHES_REGEX),
            (ContextValueType.STRING, Operator.IN_LIST),
            (ContextValueType.STRING, Operator.NOT_IN_LIST),
            (ContextValueType.INTEGER, Operator.EQUALS),
            (ContextValueType.INTEGER, Operator.NOT_EQUALS),
            (ContextValueType.INTEGER, Operator.GREATER_THAN),
            (ContextValueType.INTEGER, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.INTEGER, Operator.LESS_THAN),
            (ContextValueType.INTEGER, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.INTEGER, Operator.IN_LIST),
            (ContextValueType.INTEGER, Operator.NOT_IN_LIST),
            (ContextValueType.NUMBER, Operator.EQUALS),
            (ContextValueType.NUMBER, Operator.NOT_EQUALS),
            (ContextValueType.NUMBER, Operator.GREATER_THAN),
            (ContextValueType.NUMBER, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.NUMBER, Operator.LESS_THAN),
            (ContextValueType.NUMBER, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.NUMBER, Operator.IN_LIST),
            (ContextValueType.NUMBER, Operator.NOT_IN_LIST),
            (ContextValueType.BOOLEAN, Operator.EQUALS),
            (ContextValueType.BOOLEAN, Operator.NOT_EQUALS),
            (ContextValueType.VERSION, Operator.EQUALS),
            (ContextValueType.VERSION, Operator.NOT_EQUALS),
            (ContextValueType.VERSION, Operator.GREATER_THAN),
            (ContextValueType.VERSION, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.VERSION, Operator.LESS_THAN),
            (ContextValueType.VERSION, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.ENUM, Operator.EQUALS),
            (ContextValueType.ENUM, Operator.NOT_EQUALS),
            (ContextValueType.ENUM, Operator.IN_LIST),
            (ContextValueType.ENUM, Operator.NOT_IN_LIST),
            (ContextValueType.STRING_LIST, Operator.INTERSECTS),
            (ContextValueType.STRING_LIST, Operator.NOT_INTERSECTS),
            (ContextValueType.STRING_LIST, Operator.CONTAINS),
            (ContextValueType.STRING_LIST, Operator.NOT_CONTAINS),
            (ContextValueType.INTEGER_LIST, Operator.INTERSECTS),
            (ContextValueType.INTEGER_LIST, Operator.NOT_INTERSECTS),
            (ContextValueType.INTEGER_LIST, Operator.CONTAINS),
            (ContextValueType.INTEGER_LIST, Operator.NOT_CONTAINS),
            (ContextValueType.ENUM_LIST, Operator.INTERSECTS),
            (ContextValueType.ENUM_LIST, Operator.NOT_INTERSECTS),
            (ContextValueType.ENUM_LIST, Operator.CONTAINS),
            (ContextValueType.ENUM_LIST, Operator.NOT_CONTAINS),
        ]
        for value_type, operator in params:
            with self.subTest(value_type=value_type, operator=operator):
                common._validate_context_field_and_operator(value_type=value_type, operator=operator)

    def test_validate_context_field_and_operator__fail(self) -> None:
        params: Any = [
            (ContextValueType.STRING, Operator.GREATER_THAN),
            (ContextValueType.STRING, Operator.LESS_THAN),
            (ContextValueType.STRING, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.STRING, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.STRING, Operator.CONTAINS),
            (ContextValueType.STRING, Operator.NOT_CONTAINS),
            (ContextValueType.STRING, Operator.INTERSECTS),
            (ContextValueType.STRING, Operator.NOT_INTERSECTS),
            (ContextValueType.INTEGER, Operator.MATCHES_REGEX),
            (ContextValueType.INTEGER, Operator.CONTAINS),
            (ContextValueType.INTEGER, Operator.NOT_CONTAINS),
            (ContextValueType.INTEGER, Operator.INTERSECTS),
            (ContextValueType.INTEGER, Operator.NOT_INTERSECTS),
            (ContextValueType.NUMBER, Operator.MATCHES_REGEX),
            (ContextValueType.NUMBER, Operator.CONTAINS),
            (ContextValueType.NUMBER, Operator.NOT_CONTAINS),
            (ContextValueType.NUMBER, Operator.INTERSECTS),
            (ContextValueType.NUMBER, Operator.NOT_INTERSECTS),
            (ContextValueType.BOOLEAN, Operator.MATCHES_REGEX),
            (ContextValueType.BOOLEAN, Operator.GREATER_THAN),
            (ContextValueType.BOOLEAN, Operator.LESS_THAN),
            (ContextValueType.BOOLEAN, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.BOOLEAN, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.BOOLEAN, Operator.CONTAINS),
            (ContextValueType.BOOLEAN, Operator.NOT_CONTAINS),
            (ContextValueType.BOOLEAN, Operator.INTERSECTS),
            (ContextValueType.BOOLEAN, Operator.NOT_INTERSECTS),
            (ContextValueType.VERSION, Operator.MATCHES_REGEX),
            (ContextValueType.VERSION, Operator.CONTAINS),
            (ContextValueType.VERSION, Operator.NOT_CONTAINS),
            (ContextValueType.VERSION, Operator.INTERSECTS),
            (ContextValueType.VERSION, Operator.NOT_INTERSECTS),
            (ContextValueType.VERSION, Operator.IN_LIST),
            (ContextValueType.VERSION, Operator.NOT_IN_LIST),
            (ContextValueType.ENUM, Operator.MATCHES_REGEX),
            (ContextValueType.ENUM, Operator.GREATER_THAN),
            (ContextValueType.ENUM, Operator.LESS_THAN),
            (ContextValueType.ENUM, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.ENUM, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.ENUM, Operator.CONTAINS),
            (ContextValueType.ENUM, Operator.NOT_CONTAINS),
            (ContextValueType.ENUM, Operator.INTERSECTS),
            (ContextValueType.ENUM, Operator.NOT_INTERSECTS),
            (ContextValueType.STRING_LIST, Operator.EQUALS),
            (ContextValueType.STRING_LIST, Operator.NOT_EQUALS),
            (ContextValueType.STRING_LIST, Operator.MATCHES_REGEX),
            (ContextValueType.STRING_LIST, Operator.GREATER_THAN),
            (ContextValueType.STRING_LIST, Operator.LESS_THAN),
            (ContextValueType.STRING_LIST, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.STRING_LIST, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.STRING_LIST, Operator.IN_LIST),
            (ContextValueType.STRING_LIST, Operator.NOT_IN_LIST),
            (ContextValueType.INTEGER_LIST, Operator.EQUALS),
            (ContextValueType.INTEGER_LIST, Operator.NOT_EQUALS),
            (ContextValueType.INTEGER_LIST, Operator.MATCHES_REGEX),
            (ContextValueType.INTEGER_LIST, Operator.GREATER_THAN),
            (ContextValueType.INTEGER_LIST, Operator.LESS_THAN),
            (ContextValueType.INTEGER_LIST, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.INTEGER_LIST, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.INTEGER_LIST, Operator.IN_LIST),
            (ContextValueType.INTEGER_LIST, Operator.NOT_IN_LIST),
            (ContextValueType.ENUM_LIST, Operator.EQUALS),
            (ContextValueType.ENUM_LIST, Operator.NOT_EQUALS),
            (ContextValueType.ENUM_LIST, Operator.MATCHES_REGEX),
            (ContextValueType.ENUM_LIST, Operator.GREATER_THAN),
            (ContextValueType.ENUM_LIST, Operator.LESS_THAN),
            (ContextValueType.ENUM_LIST, Operator.LESS_THAN_OR_EQUAL_TO),
            (ContextValueType.ENUM_LIST, Operator.GREATER_THAN_OR_EQUAL_TO),
            (ContextValueType.ENUM_LIST, Operator.IN_LIST),
            (ContextValueType.ENUM_LIST, Operator.NOT_IN_LIST)
        ]
        for value_type, operator in params:
            with self.subTest(value_type=value_type, operator=operator):
                with self.assertRaises(exceptions.InvalidFeatureFlagConditions):
                    common._validate_context_field_and_operator(value_type=value_type, operator=operator)

    def test_validate_string_condition__pass(self) -> None:
        params: Any = [
            (1, Operator.EQUALS, '1'),
            ('1', Operator.EQUALS, '1'),
            ('a*b', Operator.MATCHES_REGEX, 'a*b'),
            (True, Operator.NOT_EQUALS, 'True'),
            ([1, '1', 'a*b', True], Operator.IN_LIST, ['1', '1', 'a*b', 'True']),
            ([1, '1', 'a*b', True], Operator.NOT_IN_LIST, ['1', '1', 'a*b', 'True'])
        ]
        for value, operator, expected in params:
            with self.subTest(value=value, operator=operator, expected=expected):
                actual = common._validate_string_condition(value=value, operator=operator)
                self.assertEqual(expected, actual)

    def test_validate_string_condition__fail(self) -> None:
        params: Any = [
            (None, Operator.EQUALS),
            ([1], Operator.NOT_EQUALS),
            ({'a': 1}, Operator.MATCHES_REGEX),
            ('1', Operator.IN_LIST),
            (1, Operator.NOT_IN_LIST),
            ([None], Operator.IN_LIST),
            ([{'a': 1}], Operator.NOT_IN_LIST)
        ]
        for value, operator in params:
            with self.subTest(value=value, operator=operator):
                with self.assertRaises(Exception):
                    common._validate_string_condition(value=value, operator=operator)

    def test_validate_integer_condition__pass(self) -> None:
        params: Any = [
            (1, Operator.EQUALS, 1),
            (0, Operator.EQUALS, 0),
            ('3', Operator.GREATER_THAN, 3),
            ('0', Operator.LESS_THAN_OR_EQUAL_TO, 0),
            ([1, 0, '3', '0'], Operator.IN_LIST, [1, 0, 3, 0]),
            ([1, 0, '3', '0'], Operator.NOT_IN_LIST, [1, 0, 3, 0])
        ]
        for value, operator, expected in params:
            with self.subTest(value=value, operator=operator, expected=expected):
                actual = common._validate_integer_condition(value=value, operator=operator)
                self.assertEqual(expected, actual)

    def test_validate_integer_condition__fail(self) -> None:
        params: Any = [
            (1.3, Operator.EQUALS),
            ('1.3', Operator.EQUALS),
            ('a', Operator.NOT_EQUALS),
            (True, Operator.GREATER_THAN),
            ([], Operator.LESS_THAN_OR_EQUAL_TO),
            ({}, Operator.LESS_THAN_OR_EQUAL_TO),
            (None, Operator.NOT_EQUALS),
            ([1, 0, '3', False], Operator.IN_LIST),
            ([1, 0, '3.4', '0'], Operator.NOT_IN_LIST)
        ]
        for value, operator in params:
            with self.subTest(value=value, operator=operator):
                with self.assertRaises(Exception):
                    common._validate_integer_condition(value=value, operator=operator)

    def test_validate_number_condition__pass(self) -> None:
        params: Any = [
            (1, Operator.EQUALS, 1.0),
            (0, Operator.EQUALS, 0.0),
            ('3', Operator.GREATER_THAN, 3.0),
            ('3.4', Operator.GREATER_THAN, 3.4),
            ('0', Operator.LESS_THAN_OR_EQUAL_TO, 0.0),
            ([1, 0, '3.4', '0'], Operator.IN_LIST, [1.0, 0.0, 3.4, 0.0]),
            ([1, 0, '3.4', '0'], Operator.NOT_IN_LIST, [1.0, 0.0, 3.4, 0.0])
        ]
        for value, operator, expected in params:
            with self.subTest(value=value, operator=operator, expected=expected):
                actual = common._validate_number_condition(value=value, operator=operator)
                self.assertEqual(expected, actual)

    def test_validate_number_condition__fail(self) -> None:
        params: Any = [
            ('a', Operator.NOT_EQUALS),
            (True, Operator.GREATER_THAN),
            ([], Operator.LESS_THAN_OR_EQUAL_TO),
            ({}, Operator.LESS_THAN_OR_EQUAL_TO),
            (None, Operator.NOT_EQUALS),
            ([1, 0, '3', False], Operator.IN_LIST),
            ([1, 0, None, '0'], Operator.NOT_IN_LIST)
        ]
        for value, operator in params:
            with self.subTest(value=value, operator=operator):
                with self.assertRaises(Exception):
                    common._validate_number_condition(value=value, operator=operator)

    def test_validate_boolean_condition__pass(self) -> None:
        params: Any = [
            ('tRue', True),
            ('fAlse', False),
            (True, True),
            (False, False)
        ]
        for value, expected in params:
            with self.subTest(value=value, expected=expected):
                actual = common._validate_boolean_condition(value=value)
                self.assertEqual(expected, actual)

    def test_validate_boolean_condition__fail(self) -> None:
        params: Any = [
            'blah',
            0,
            1.4,
            [],
            {},
            None
        ]
        for value in params:
            with self.subTest(value=value):
                with self.assertRaises(Exception):
                    common._validate_boolean_condition(value=value)

    def test_validate_version_condition__pass(self) -> None:
        params: Any = [
            ('1', '1'),
            ('1.2', '1.2'),
            ('1.2.3', '1.2.3')
        ]
        for value, expected in params:
            with self.subTest(value=value, expected=expected):
                actual = common._validate_version_condition(value=value)
                self.assertEqual(expected, actual)

    def test_validate_version_condition__fail(self) -> None:
        params: Any = [
            1,
            1.2,
            None,
            [],
            {},
            False
        ]
        for value in params:
            with self.subTest(value=value):
                with self.assertRaises(Exception):
                    common._validate_version_condition(value=value)

    def test_validate_enum_condition__pass(self) -> None:
        params: Any = [
            (Operator.EQUALS, 1, {'a': 1}, 1),
            (Operator.NOT_EQUALS, '1', {'a': '1'}, '1'),
            (Operator.IN_LIST, [1], {'a': 1}, [1]),
            (Operator.NOT_IN_LIST, ['1'], {'a': '1'}, ['1'])
        ]
        for operator, value, enum_def, expected in params:
            with self.subTest(operator=operator, value=value, enum_def=enum_def, expected=expected):
                actual = common._validate_enum_condition(operator=operator, value=value, enum_def=enum_def)
                self.assertEqual(expected, actual)

    def test_validate_enum_condition__fail(self) -> None:
        params: Any = [
            (Operator.EQUALS, 1, {'a': '1'}),
            (Operator.NOT_EQUALS, '1', {'a': 1}),
            (Operator.NOT_EQUALS, None, {'a': 1}),
            (Operator.EQUALS, False, {'a': 1}),
            (Operator.NOT_EQUALS, 1.2, {'a': 1}),
            (Operator.IN_LIST, [1], {'a': '1'}),
            (Operator.NOT_IN_LIST, ['1'], {'a': 1})
        ]
        for operator, value, enum_def in params:
            with self.subTest(operator=operator, value=value, enum_def=enum_def):
                with self.assertRaises(Exception):
                    common._validate_enum_condition(operator=operator, value=value, enum_def=enum_def)

    def test_validate_string_list_condition__pass(self) -> None:
        params: Any = [
            (Operator.CONTAINS, 'a', 'a'),
            (Operator.NOT_CONTAINS, 1, '1'),
            (Operator.CONTAINS, 1.4, '1.4'),
            (Operator.NOT_CONTAINS, True, 'True'),
            (Operator.INTERSECTS, ['a'], ['a']),
            (Operator.NOT_INTERSECTS, [1], ['1']),
            (Operator.INTERSECTS, [1.4], ['1.4']),
            (Operator.NOT_INTERSECTS, [True], ['True']),
            (Operator.INTERSECTS, [], []),
        ]
        for operator, value, expected in params:
            with self.subTest(value=value, operator=operator, expected=expected):
                actual = common._validate_string_list_condition(value=value, operator=operator)
                self.assertEqual(expected, actual)

    def test_validate_string_list_condition__fail(self) -> None:
        params: Any = [
            (Operator.CONTAINS, None),
            (Operator.NOT_CONTAINS, []),
            (Operator.NOT_CONTAINS, {}),
            (Operator.INTERSECTS, 'a'),
            (Operator.NOT_INTERSECTS, 1),
            (Operator.INTERSECTS, {})
        ]
        for operator, value in params:
            with self.subTest(value=value, operator=operator):
                with self.assertRaises(Exception):
                    common._validate_string_list_condition(value=value, operator=operator)

    def test_validate_integer_list_condition__pass(self) -> None:
        params: Any = [
            (Operator.CONTAINS, '1', 1),
            (Operator.NOT_CONTAINS, 1, 1),
            (Operator.INTERSECTS, ['1'], [1]),
            (Operator.NOT_INTERSECTS, [1], [1]),
            (Operator.NOT_INTERSECTS, [], [])
        ]
        for operator, value, expected in params:
            with self.subTest(value=value, operator=operator, expected=expected):
                actual = common._validate_integer_list_condition(value=value, operator=operator)
                self.assertEqual(expected, actual)

    def test_validate_integer_list_condition__fail(self) -> None:
        params: Any = [
            (Operator.CONTAINS, '1.2'),
            (Operator.CONTAINS, 'a'),
            (Operator.NOT_CONTAINS, 1.2),
            (Operator.CONTAINS, None),
            (Operator.NOT_CONTAINS, False),
            (Operator.CONTAINS, []),
            (Operator.NOT_CONTAINS, {}),
            (Operator.INTERSECTS, ['1.2']),
            (Operator.NOT_INTERSECTS, [1.2]),
            (Operator.INTERSECTS, ['a']),
            (Operator.NOT_INTERSECTS, [None]),
            (Operator.INTERSECTS, [False]),
            (Operator.NOT_INTERSECTS, [[]]),
            (Operator.NOT_INTERSECTS, [{}])
        ]
        for operator, value in params:
            with self.subTest(value=value, operator=operator):
                with self.assertRaises(Exception):
                    common._validate_integer_list_condition(value=value, operator=operator)

    def test_validate_enum_list_condition__pass(self) -> None:
        params: Any = [
            (Operator.CONTAINS, 1, {'a': 1}, 1),
            (Operator.NOT_CONTAINS, '1', {'a': '1'}, '1'),
            (Operator.INTERSECTS, [1], {'a': 1}, [1]),
            (Operator.NOT_INTERSECTS, ['1'], {'a': '1'}, ['1']),
            (Operator.NOT_INTERSECTS, [], {'a': '1'}, [])
        ]
        for operator, value, enum_def, expected in params:
            with self.subTest(operator=operator, value=value, enum_def=enum_def, expected=expected):
                actual = common._validate_enum_list_condition(operator=operator, value=value, enum_def=enum_def)
                self.assertEqual(expected, actual)

    def test_validate_enum_list_condition__fail(self) -> None:
        params: Any = [
            (Operator.CONTAINS, '1', {'a': 1}),
            (Operator.NOT_CONTAINS, 1, {'a': '1'}),
            (Operator.NOT_CONTAINS, None, {'a': '1'}),
            (Operator.NOT_CONTAINS, False, {'a': 1}),
            (Operator.NOT_CONTAINS, [], {'a': '1'}),
            (Operator.NOT_CONTAINS, {}, {'a': '1'}),
            (Operator.INTERSECTS, ['1'], {'a': 1}),
            (Operator.NOT_INTERSECTS, [1], {'a': '1'}),
            (Operator.NOT_INTERSECTS, [None], {'a': '1'}),
            (Operator.NOT_INTERSECTS, [False], {'a': 1}),
            (Operator.NOT_INTERSECTS, [[]], {'a': '1'}),
            (Operator.NOT_INTERSECTS, [{}], {'a': '1'})
        ]
        for operator, value, enum_def in params:
            with self.subTest(operator=operator, value=value, enum_def=enum_def):
                with self.assertRaises(Exception):
                    common._validate_enum_list_condition(operator=operator, value=value, enum_def=enum_def)
