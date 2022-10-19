from formfiller import FormFiller
import argparse
import sys


# call via python -m formfiller
def cli(args):
    ff = FormFiller(**vars(args))
    sys.stdout.buffer.write(ff.as_png())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=str, help="path to payload json file")
    parser.add_argument("--form", type=str, help="path to form definition json file")
    parser.add_argument("--image", type=str, help="path to base form image file")
    parser.add_argument(
        "--font",
        type=str,
        default="Liberation-Sans",
        help="font name (default Liberation-Sans)",
    )
    parser.add_argument(
        "--font-size", type=int, default=24, help="font size (default 24)"
    )
    parser.add_argument(
        "--font-color", type=str, default="blue", help="font color (default blue)"
    )
    cli(parser.parse_args())
