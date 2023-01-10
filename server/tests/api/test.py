import ujson
from typing import cast, Any, Iterable
from rest_api_tester.test import TestCase as BaseTestCase, TestResult


class TestCase(BaseTestCase):

    DEFAULT_IGNORE_FIELDS = ('_id', 'created_date', 'updated_date')

    def setUp(self) -> None:
        self.maxDiff = None

    def ignore_expected_response_fields(
        self,
        result: TestResult,
        fields: Iterable[str]
    ) -> str | None:
        actual_response_dict = result.response.json()
        if result.test_data.expected_response and result.response.status_code == 200:
            expected_response_dict = ujson.loads(result.test_data.expected_response)
            for field in fields:
                if field in actual_response_dict and expected_response_dict[field] is None:
                    self.assertIsNotNone(actual_response_dict[field])
                    expected_response_dict[field] = actual_response_dict[field]
            result.test_data.expected_response = ujson.dumps(expected_response_dict)

        return cast(str | None, actual_response_dict.get('_id'))

    @staticmethod
    def replace_response_strings(
        result: TestResult,
        **kwargs: Any
    ) -> None:
        expected_response = result.test_data.expected_response
        if expected_response:
            for key, value in kwargs.items():
                expected_response = expected_response.replace(f'%%{key}%%', str(value))

        result.test_data.expected_response = expected_response
