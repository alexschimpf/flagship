import unittest
from typing import Any

from app.api.exceptions.exceptions import InvalidEnumDefException
from app.api.routes.context_fields.controllers import common


class TestContextFieldsCommon(unittest.TestCase):

    def test_validate_enum_def__pass(self) -> None:
        params: Any = [
            None,
            {'a': 1, 'b': 2},
            {'a': 1.2, 'b': 2.3},
            {'a': 'A', 'b': 'B'}
        ]
        for enum_def in params:
            with self.subTest(enum_def=enum_def):
                common.validate_enum_def(enum_def=enum_def)

    def test_validate_enum_def__fail(self) -> None:
        params: Any = [
            {'a': 1, 'b': '1'},
            {},
            {'a': ''},
            {'a': '  '},
            {'a': None},
            {'a': True}
        ]
        for enum_def in params:
            with self.subTest(enum_def=enum_def):
                with self.assertRaises(InvalidEnumDefException):
                    common.validate_enum_def(enum_def=enum_def)
