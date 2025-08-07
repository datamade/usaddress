import typing

def parse(address_string: str) -> list[tuple[str, str]]:
    """
    Split an address string into components, and label each component.

    Args:
        address_string (str): The address to parse

    Returns:
        list[ tuple[str, str] ]: The parsed address
    """
    ...

def tag(address_string: str, tag_mapping=None) -> tuple[dict[str, str], str]:
    """
    Parse and merge consecutive components & strip commas.
    Also return an address type (`Street Address`, `Intersection`, `PO Box`, or `Ambiguous`).

    Because this method returns an OrderedDict with labels as keys, it will throw a
    `RepeatedLabelError` error when multiple areas of an address have the same label,
    and thus can't be concatenated. When `RepeatedLabelError` is raised, it is likely
    that either (1) the input string is not a valid address, or (2) some tokens were
    labeled incorrectly.

    It is also possible to pass a mapping dict to this method to remap the labels to your own format.

    Args:
        address_string (str): The address to parse
        tag_mapping (dict): Optional - The tags you'd like to remap, formatted as: `{'OldTag': 'NewTag'}`

    Returns:
        tuple[ dict[str, str], str ]: The tagged address

    """
    ...

def tokenize(address_string: str) -> list[str]:
    """
    Split each component of an address into a list of unlabeled tokens.

    Args:
        address_string (str): The address to tokenize

    Returns:
        list[str]: The tokenized address
    """
    ...

Feature = dict[str, typing.Union[str, bool, "Feature"]]

def tokenFeatures(token: str) -> Feature:
    """
    Return a `Feature` dict with attributes that describe a token.

    Args:
        token (str): The token to analyze

    Returns:
        Feature: A type of dict with attributes that describe the token
        (`abbrev`, `digits`, `word`, `trailing.zeros`, `length`, `endsinpunc`, `directional`, `street_name`, `has.vowels`)
    """
    ...

def tokens2features(address: list[str]) -> list[Feature]:
    """
    Turn every token into a `Feature` dict, and return a list of each token as a `Feature`.
    Each attribute in a `Feature` describes the corresponding token.

    Args:
        address list[str]: The address as a list of tokens.

    Returns:
        list[Feature]: A list of all tokens with various details about each one.
    """
    ...

def digits(token: str) -> typing.Literal["all_digits", "some_digits", "no_digits"]:
    """
    Identify whether the token string is all digits, has some digits, or has no digits

    Args:
        token (str): The token to parse

    Returns:
        str: A label denoting the presence of digits in the token (`all_digits`, `some_digits`, or `no_digits`)
    """
    ...

# for some reason mypy can't believe that this will return a str as of 10/2024
def trailingZeros(token: str) -> str:
    """
    Return any trailing zeros found at the end of a token.
    If none are found, then return an empty string.

    Args:
        token (str): The token to search for zeros.

    Returns:
        str: The trailing zeros found, if any. Otherwise, an empty string.
    """
    ...
