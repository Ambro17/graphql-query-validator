# graphql-query-validator
Validate queries against a given schema

## Run validation
```
python main.py schema.gql queries.json
```
Outputs:
```
Cannot query field 'delete_name' on type 'Mutation'.
Cannot query field 'name' on type 'User'.
```

## Verbose mode
```
python main.py schema.gql queries.json -v
```
Outputs:
```
[
    {
        "message": "Cannot query field 'delete_name' on type 'Mutation'.",
        "locations": [
            {
                "line": 1,
                "column": 29
            }
        ],
        "path": null,
        "source": "mutation DeleteIt($id:Int!){delete_name(id:$id){__typename id}}"
    },
    {
        "message": "Cannot query field 'name' on type 'User'.",
        "locations": [
            {
                "line": 1,
                "column": 24
            }
        ],
        "path": null,
        "source": "query MyQuery{users{id name}}"
    }
]
```

## Dump errors to json file
```
python main.py schema.gql queries.json -v > errors.json
```

## Exit code
The script follows process conventions and outputs `0` as the exit code if all queries are valid and `1` if at least one query can't be resolved by the schema
