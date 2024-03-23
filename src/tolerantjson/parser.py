import json


class ParseError(Exception):
    pass


def tolerate(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        data, reminding = parse_any(s, e)
        tolerate.last_parse_reminding = reminding
        if tolerate.on_extra_token and len(reminding) > 0:
            tolerate.on_extra_token(s, data, reminding)
        return data


tolerate.last_parse_reminding = None
tolerate.on_extra_token = lambda text, data, reminding: print(
    f"parsed json with extra tokens: text={text}, data={data}, reminding={reminding}"
)


def parse_any(s, e):
    parser = parsers.get(s[0])
    if not parser:
        # no parser registered for s[0]
        raise ParseError(e)
    return parser(s, e)


def skip_space(s):
    return s.lstrip()


def parse_space(s, e):
    s = skip_space(s)
    return parse_any(s, e)


def parse_array(s, e):
    s = s[1:]  # skip starting '['
    acc = []
    s = skip_space(s)
    while s:
        if s[0] == "]":
            s = s[1:]  # skip ending ']'
            break
        res = parse_any(s, e)
        acc.append(res[0])
        s = res[1]
        s = skip_space(s)
        if len(s) > 0 and s[0] == ",":
            s = s[1:]
            s = skip_space(s)
    return [acc, s]


def parse_number(s, e):
    for i in range(len(s)):
        c = s[i]
        if parsers.get(c) != parse_number:
            num = s[:i]
            s = s[i:]
            return [num_to_str(num), s]
    return [num_to_str(s), ""]


def num_to_str(s):
    if s == "-":
        return -0
    try:
        num = float(s)
        if num.is_integer():
            return int(num)
        return num
    except ValueError:
        return s


def parse_string(s, e):
    for i in range(1, len(s)):
        c = s[i]
        if c == "\\":
            i += 1
            continue
        if c == '"':
            string = s[: i + 1]
            s = s[i + 1 :]
            return [json.loads(string), s]
    return [json.loads(s + '"'), ""]


def parse_object(s, e):
    s = s[1:]  # skip starting '{'
    acc = {}
    s = skip_space(s)
    while s:
        if s[0] == "}":
            s = s[1:]  # skip ending '}'
            break

        key_res = parse_any(s, e)
        key = key_res[0]
        s = key_res[1]

        s = skip_space(s)
        if s[0] != ":":
            acc[key] = None
            break
        s = s[1:]  # skip ':'
        s = skip_space(s)

        if not s:
            acc[key] = None
            break
        value_res = parse_any(s, e)
        acc[key] = value_res[0]
        s = value_res[1]
        s = skip_space(s)
        if len(s) > 0 and s[0] == ",":
            s = s[1:]
            s = skip_space(s)
    return [acc, s]


def parse_true(s, e):
    return parse_token(s, "true", True, e)


def parse_false(s, e):
    return parse_token(s, "false", False, e)


def parse_null(s, e):
    return parse_token(s, "null", None, e)


def parse_token(s, token_str, token_val, e):
    for i in range(len(token_str), 0, -1):
        if s.startswith(token_str[:i]):
            return [token_val, s[i:]]
    prefix = json.dumps(s[: len(token_str)])
    # unknown token starting with prefix
    raise ParseError(e)


parsers = {}
parsers[" "] = parse_space
parsers["\r"] = parse_space
parsers["\n"] = parse_space
parsers["\t"] = parse_space
parsers["["] = parse_array
for c in "0123456789.-":
    parsers[c] = parse_number
parsers['"'] = parse_string
parsers["{"] = parse_object
parsers["t"] = parse_true
parsers["f"] = parse_false
parsers["n"] = parse_null
