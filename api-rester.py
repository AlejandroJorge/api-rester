import argparse
from lib.api_runner import BaseAPIRunner, DebugAPIRunner


if __name__ == '__main__':
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

    APIRunner = DebugAPIRunner if args.v else BaseAPIRunner

    api_runner_args = {
        "request_filename": args.req,
        "response_filename": args.res
    }

    api_runner = APIRunner(**api_runner_args)

    api_runner.execute()
