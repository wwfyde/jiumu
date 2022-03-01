from typing import List
import logging

log = logging.getLogger('demo')


def process_items(items: List[str]):
    for item in items:
        log.info(f"{item}, {item.upper()}")
        print(item.upper())


if __name__ == '__main__':
    process_items(['ABC', 'aBc', 'AaA'])
