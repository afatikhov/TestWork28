import logging

logger = logging.getLogger("quotes_parser")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("../logs/quotes_parser.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)