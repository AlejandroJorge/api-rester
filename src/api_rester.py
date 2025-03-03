import argparse
from dotenv import load_dotenv

from lib.api_runner import BaseAPIRunner
from lib.config import app_config

from lib.template import write_template
from lib.util import clear_files


def main():
    load_dotenv(dotenv_path=".env")

    parser = argparse.ArgumentParser(
        prog="api-rester",
        description="A simple REST API CLI Client"
    )

    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        title='Available commands'
    )

    call_parser = subparsers.add_parser("call", help="Execute API call")

    call_parser.add_argument('--req', '--request-filename',
                             default='request.json')
    call_parser.add_argument('--res', '--response-filename',
                             default='response.json')
    call_parser.add_argument('--cookies', '--cookies-filename',
                             default='cookies.json')
    call_parser.add_argument(
        '--v', '--verbose', action='store_true', default=False)

    template_parser = subparsers.add_parser(
        "template", help="Generate request template")

    template_parser.add_argument("--f", "--filename", default="request.json",
                                 help="Name of the file where the template will be generated")

    cookies_parser = subparsers.add_parser(
        "clear", help="Clear request file, response file and cookie file")
    cookies_parser.add_argument(
        "--req", "--request-filename", default="request.json",
        help="Name of the file where the request is stored")
    cookies_parser.add_argument(
        "--res", "--response-filename", default="response.json",
        help="Name of the file where the response is stored")
    cookies_parser.add_argument(
        "--cookies", "--cookies-filename", default="cookies.json",
        help="Name of the file where the cookies state is stored")

    args = parser.parse_args()

    if args.command == 'call':
        app_config.verbose = args.v
        api_runner = BaseAPIRunner(
            request_filename=args.req,
            response_filename=args.res,
            cookies_filename=args.cookies)
        api_runner.execute()

    elif args.command == 'template':
        write_template(args.f)

    elif args.command == 'clear':
        clear_files(req_filename=args.req,
                    res_filename=args.res,
                    cookies_filename=args.cookies)


if __name__ == '__main__':
    main()
