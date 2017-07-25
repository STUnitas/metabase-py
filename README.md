# metabase-py

python wrapper for metabase api

## Installation

```bash
pip install metabase
```

## How to use

```python
import pprint
from metabase import Metabase

metabase = Metabase(email="<email>", password="<password>")

# get all cards
pprint.pprint(metabase.get("/card/"))

payload={
        'dataset_query': {
            'database': 2,
            'native': {
                'query': "SELECT 1,2,3;" },
            'type': 'native' },
        'display': "area",
        'name': 'test:1',
        'visualization_settings': {
        'graph.dimensions': ['a'],
        'graph.metrics': ['b', 'c'],
	'graph.show_goal': False,
        'line.interpolate': 'linear',
        'line.marker_enabled': True,
	'line.missing': 'interpolate',
	'stackable.stack_type': 'stacked',
	'table.column_widths': [] }}

pprint.pprint(metabase.post("/card/", json=payload))
pprint.pprint(metabase.get("/card/"))
```

## Environments

- `METABASE_ENDPOINT`
- `METABASE_AUTH_EMAIL`
- `METABASE_AUTH_PASSWORD`

## Methods

- `get(<URL>, params=data)`
- `post(<URL>, json=data)`
- `head(<URL>, ...)`
- `delete(<URL>, ...)`

## Features

- can set `session key` as manually
- `auth_callback` authentication callback (For custom storage)

## Notice

This library wraps [requests](http://docs.python-requests.org/en/master/)

## Contributors

see [here](https://github.com/STUnitas/metabase-py/graphs/contributors)
