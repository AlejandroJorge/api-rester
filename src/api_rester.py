import argparse

from lib.api_runner import BaseAPIRunner
from lib.config import app_config


def main():
    parser = argparse.ArgumentParser(
        prog="api-rester",
        description="CLI API REST Client"
    )

    parser.add_argument('--req', '--request-filename',
                        default='request.json')
    parser.add_argument('--res', '--response-filename',
                        default='response.json')
    parser.add_argument('--v', '--verbose', action='store_true', default=False)

    args = parser.parse_args()

    app_config.verbose = args.v

    api_runner = BaseAPIRunner(
        request_filename=args.req, response_filename=args.res)

    api_runner.execute()


if __name__ == '__main__':
    main()
