#/bin/python3
import argparse
from internals import process_api_rest_request

parser = argparse.ArgumentParser()

parser.add_argument('request_name', help='indicates input files {request_name}_request_data.json and {request_name}_request_body.json and output files {request_name}_response_data.json and {request_name}_response_body.json', type=str)

args = parser.parse_args()

process_api_rest_request(args.request_name, args.request_name)
