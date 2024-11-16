from logging import LogRecord
from json_log_formatter import JSONFormatter


class CustomJSONFormatter(JSONFormatter):
    def json_record(self, message: str, extra: dict, record: LogRecord) -> dict:
        extra["time"] = self.formatTime(record)
        extra["level"] = record.levelname
        extra["message"] = message
        return extra
