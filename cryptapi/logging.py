import logging

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;63m[\x1b[0m%(asctime)s\x1b[38;5;63m]\x1b[0m %(message)s",
    datefmt="%H:%M:%S"
)