import logging


def main() -> int:
    logging.info("Hello world")
    return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
