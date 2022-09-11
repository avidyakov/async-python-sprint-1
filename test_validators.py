from validators import ResponseValidator


class TestResponseValidator:
    def test_validate_response(self, response_path):
        validator = ResponseValidator.parse_file(response_path)

        assert len(validator.forecasts) == 5
        assert validator.forecasts[0].hours[0].hour == 9
        assert validator.forecasts[0].hours[-1].hour == 19
        assert len(validator.forecasts[0].hours) == 11
