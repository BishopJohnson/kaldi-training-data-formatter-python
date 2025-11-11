import sys

from src.kaldi_training_data_formatter import App


def main() -> int:
    return App().run()


if __name__ == '__main__':
    sys.exit(main())
