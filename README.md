# tolerantjson

`tolerantjson` is a Python package that provides a robust JSON parser capable of handling non-standard JSON inputs. This parser is designed to be more forgiving than the strict JSON parsers that adhere to the RFC 7159 specification. It can handle certain forms of malformed JSON, such as trailing commas or single-quoted strings, and can provide callbacks for dealing with extra tokens.

## Features
- Parses JSON with a best-effort, recovering from some common errors in JSON formatting.
- Reports the nature and position of parsing errors for easier debugging.
- Provides a mechanism to handle extra tokens or malformed structures via callbacks.
- Register custom parsers for specific cases or tokens.

## Installation

To install `tolerantjson`, use pip:

```bash
pip install tolerantjson
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/nurettn/tolerantjson.git
cd tolerantjson
python setup.py install
```


## Usage
Here is a basic example of how to use tolerantjson to parse a JSON string:

```python3
import tolerantjson as tjson

# Example JSON string with an error
json_str = '[1,2,{"a":"apple",}]'

# Parse the JSON string
try:
    data = tjson.tolerate(json_str)
    print(data)
except tjson.ParseException as e:
    print(f"Failed to parse JSON: {e}")

# Output: [1, 2, {'a': 'apple'}]
```

## Handling Extra Tokens
You can define your own callback for handling extra tokens by assigning a function to `tjson.parse.on_extra_token`. Here's an example:

```python3
import tolerantjson as tjson


def handle_extra_token(text, data, reminding):
    print(f"Warning: Extra tokens detected after valid JSON. Data: {data}, Extra: {reminding}")


# Assign your custom callback
tjson.tolerate.on_extra_token = handle_extra_token

# Parse a JSON string with extra tokens
json_str = '[1,2,3] extra tokens'
data = tjson.tolerate(json_str)
``` 


## Custom Parsers
You can extend `tolerantjson` with custom parsers for specific scenarios:

```python3
import tolerantjson as tjson


def parse_custom_date(s, e):
    # Custom parsing logic
    pass


# Register the custom parser for a specific token
tjson.parsers['d'] = parse_custom_date

# Use the extended parser
json_str = 'd"2024-03-22"'
data = tjson.tolerate(json_str)
``` 

## Contribution
Contributions are welcome! If you would like to contribute to the project, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or fix.
- Write your code and add tests if applicable.
- Submit a pull request with a clear description of your changes.

##  License
`tolerantjson` is open source software licensed as MIT.

##  Credits
This project was inspired by the [best-effort-json-parser](https://www.npmjs.com/package/best-effort-json-parser).