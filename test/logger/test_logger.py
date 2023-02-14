import pytest
from starlette.requests import Request
from starlette.datastructures import Headers

# import internal modules
from surquest.GCP.logger import Logger

trace = "4ab5b3118c3e7cad6fef2b9376ecb9b0/2141214;o=0"
request = Request(
    {
        "type": "http",
        "path": "/my/path",
        "headers": Headers({
            "x-cloud-trace-context": trace
        }).raw,
        "http_version": "1.1",
        "method": "GET",
        "scheme": "https",
        "client": ("127.0.0.1", 8080),
        "server": ("www.example.com", 443),
    }
)


class TestLogger:

    LOGGER = Logger()
    ERRORS = {
        "value": "Wrong value: Expected: `{}`, Actual: `{}`",
        "type": "Wrong type: Expected: `{}`, Actual: `{}`"
    }

    @pytest.mark.parametrize(
        "params,expected",
        [
            (
                {
                    "severity": "DEBUG",
                    "msg": "This is a DEBUG message",
                    "ctx": {}
                },
                {
                    "type": dict
                }
            )
        ]
    )
    def test__log(self, params, expected):

        entry = self.LOGGER.log(
            severity=params.get("severity"),
            msg=params.get("msg"),
            **params.get("ctx")
        )

        assert expected.get("type") == type(entry), \
            self.ERRORS.get("type").format(
                expected.get("type"),
                type(entry)
            )

        assert params.get("severity") == entry.get("severity"), \
            self.ERRORS.get("value").format(
                params.get("severity"),
                entry.get("severity")
            )

        assert params.get("msg") == entry.get("message"), \
            self.ERRORS.get("value").format(
                params.get("msg"),
                entry.get("message")
            )


    @pytest.mark.parametrize(
        "level,expected",
        [
            ("DEBUG", dict),
            ("INFO", dict),
            ("WARNING", dict),
            ("ERROR", dict),
            ("CRITICAL", dict),
            (100, dict),
            (200, dict),
            (300, dict),
            (400, dict),
            (500, dict),
        ]
    )
    def test__log_level(self, level, expected):

        log_level = self.LOGGER.get_log_level(level)

        assert type(log_level) == expected, \
            self.ERRORS.get("type").format(
                expected,
                type(log_level)
            )


        log_level_value = self.LOGGER.get_log_level_value(level)

        assert type(log_level_value) == int, \
            self.ERRORS.get("type").format(
                int,
                type(log_level_value)
            )

    def test__debug(self):

        msg = "This is a DEBUG message"
        entry = self.LOGGER.debug(msg)

        assert type(entry) == dict, \
            self.ERRORS.get("type").format(
                dict,
                type(entry)
            )

        assert "DEBUG" == entry.get("severity"), \
            self.ERRORS.get("value").format(
                "DEBUG",
                entry.get("severity")
            )

        assert msg == entry.get("message"), \
            self.ERRORS.get("value").format(
                msg,
                entry.get("message")
            )

        assert None == entry.get("context"), \
            self.ERRORS.get("value").format(
                None,
                entry.get("context")
            )

    def test__warning(self):

        entry = self.LOGGER.warning(
            "This is a WARNING message",
            **{
                "key": "value"
            }
        )

        assert type(entry) == dict, \
            self.ERRORS.get("type").format(
                dict,
                type(entry)
            )

        assert "WARNING" == entry.get("severity"), \
            self.ERRORS.get("value").format(
                "WARNING",
                entry.get("severity")
            )

        assert dict == type(entry.get("context")), \
            self.ERRORS.get("type").format(
                dict,
                type(entry.get("context"))
            )

    def test__error(self):

        entry = self.LOGGER.error(
            "This is a ERROR message",
            ctx={
                "key": "value"
            }
        )

        assert type(entry) == dict, \
            self.ERRORS.get("type").format(
                dict,
                type(entry)
            )

        assert "ERROR" == entry.get("severity"), \
            self.ERRORS.get("value").format(
                "ERROR",
                entry.get("severity")
            )

        assert dict == type(entry.get("context")), \
            self.ERRORS.get("type").format(
                dict,
                type(entry.get("context"))
            )
