import json_log_formatter

class CustomJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra['time'] = self.formatTime(record)
        extra['level'] = record.levelname
        extra['message'] = message
        return extra
