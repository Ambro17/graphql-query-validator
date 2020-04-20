import sys
import argparse
from graphql import build_schema, validate, parse, GraphQLError, GraphQLSchema
from typing import List
import json

def cli():
    args = parse_args(sys.argv[1:])
    return main(args)


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='Schema comparator')
    parser.add_argument('SCHEMA',
                        type=argparse.FileType('r', encoding='UTF-8'),
                        help='Path to the schema SDL')
    parser.add_argument('QUERIES',
                        type=argparse.FileType('r', encoding='UTF-8'),
                        help='Path to the apollo queries.json file')

    parser.add_argument("-v",
                        dest='verbose',
                        help="Output more detailed infractions",
                        action="store_true")

    return parser.parse_args(arguments)


def validate_queries_against_schema(schema, queries: List[str]) -> List[GraphQLError]:
    errors = []
    for query in queries:
        query_errors = validate(schema, parse(query))

        for e in query_errors:
            e.source_query = query

        errors.extend(query_errors)
    
    return errors


def format_error(e):
    error = e.formatted
    error['source'] = e.source_query
    return error


def pretty_print(errors: List[GraphQLError], verbose=False) -> None:
    if verbose:
        return print(
            json.dumps([format_error(e) for e in errors], indent=4)
        )
    else:
        print('\n'.join(e.message for e in errors))


def load_queries_from_file(content):
    """
    Sample input:
    {
        "version": 2,
        "operations": [
            {
                "signature": "fb094f9a6226426e2b821979465bad784f159e43f9af95deb0b4ef3b02878485",
                "document": "mutation MyMutation($id:Int!){delete(id:$id){__typename id}}",
                "metadata": {
                    "engineSignature": ""
                }
            },
            ...
        ]    
    """
    queries = json.loads(content)
    return [q['document'] for q in queries['operations']]

def main(args) -> int:
    schema = build_schema(args.SCHEMA.read())
    queries = load_queries_from_file(args.QUERIES.read())
    args.SCHEMA.close()
    args.QUERIES.close()

    errors = validate_queries_against_schema(schema, queries)
    pretty_print(errors, args.verbose)

    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(cli())