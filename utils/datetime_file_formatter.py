"""
    Custom formatted for file logs
"""
import logging

class DateTimeFileFormatter(logging.Formatter):
    """Custom formatter for file logs"""

    format_str = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: format_str,
        logging.INFO: format_str,
        logging.WARNING: format_str,
        logging.ERROR: format_str,
        logging.CRITICAL: format_str
    }

    def format(self, record : any):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
