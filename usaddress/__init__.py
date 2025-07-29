import os
import re
import string
import typing
import warnings

import probableparsing
import pycrfsuite

# The address components are based upon the `United States Thoroughfare,
# Landmark, and Postal Address Data Standard
# http://www.urisa.org/advocacy/united-states-thoroughfare-landmark-and-postal-address-data-standard

LABELS = [
    "AddressNumberPrefix",
    "AddressNumber",
    "AddressNumberSuffix",
    "StreetNamePreModifier",
    "StreetNamePreDirectional",
    "StreetNamePreType",
    "StreetName",
    "StreetNamePostType",
    "StreetNamePostDirectional",
    "SubaddressType",
    "SubaddressIdentifier",
    "BuildingName",
    "OccupancyType",
    "OccupancyIdentifier",
    "CornerOf",
    "LandmarkName",
    "PlaceName",
    "StateName",
    "ZipCode",
    "USPSBoxType",
    "USPSBoxID",
    "USPSBoxGroupType",
    "USPSBoxGroupID",
    "IntersectionSeparator",
    "Recipient",
    "NotAddress",
]

PARENT_LABEL = "AddressString"
GROUP_LABEL = "AddressCollection"

MODEL_FILE = "usaddr.crfsuite"
MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + "/" + MODEL_FILE

DIRECTIONS = {
    "n",
    "s",
    "e",
    "w",
    "ne",
    "nw",
    "se",
    "sw",
    "north",
    "south",
    "east",
    "west",
    "northeast",
    "northwest",
    "southeast",
    "southwest",
}

STREET_NAMES = {
    "allee",
    "alley",
    "ally",
    "aly",
    "anex",
    "annex",
    "annx",
    "anx",
    "arc",
    "arcade",
    "av",
    "ave",
    "aven",
    "avenu",
    "avenue",
    "avn",
    "avnue",
    "bayoo",
    "bayou",
    "bch",
    "beach",
    "bend",
    "bg",
    "bgs",
    "bl",
    "blf",
    "blfs",
    "bluf",
    "bluff",
    "bluffs",
    "blvd",
    "bnd",
    "bot",
    "bottm",
    "bottom",
    "boul",
    "boulevard",
    "boulv",
    "br",
    "branch",
    "brdge",
    "brg",
    "bridge",
    "brk",
    "brks",
    "brnch",
    "brook",
    "brooks",
    "btm",
    "burg",
    "burgs",
    "byp",
    "bypa",
    "bypas",
    "bypass",
    "byps",
    "byu",
    "camp",
    "canyn",
    "canyon",
    "cape",
    "causeway",
    "causwa",
    "causway",
    "cen",
    "cent",
    "center",
    "centers",
    "centr",
    "centre",
    "ci",
    "cir",
    "circ",
    "circl",
    "circle",
    "circles",
    "cirs",
    "ck",
    "clb",
    "clf",
    "clfs",
    "cliff",
    "cliffs",
    "club",
    "cmn",
    "cmns",
    "cmp",
    "cnter",
    "cntr",
    "cnyn",
    "common",
    "commons",
    "cor",
    "corner",
    "corners",
    "cors",
    "course",
    "court",
    "courts",
    "cove",
    "coves",
    "cp",
    "cpe",
    "cr",
    "crcl",
    "crcle",
    "crecent",
    "creek",
    "cres",
    "crescent",
    "cresent",
    "crest",
    "crk",
    "crossing",
    "crossroad",
    "crossroads",
    "crscnt",
    "crse",
    "crsent",
    "crsnt",
    "crssing",
    "crssng",
    "crst",
    "crt",
    "cswy",
    "ct",
    "ctr",
    "ctrs",
    "cts",
    "curv",
    "curve",
    "cv",
    "cvs",
    "cyn",
    "dale",
    "dam",
    "div",
    "divide",
    "dl",
    "dm",
    "dr",
    "driv",
    "drive",
    "drives",
    "drs",
    "drv",
    "dv",
    "dvd",
    "est",
    "estate",
    "estates",
    "ests",
    "ex",
    "exp",
    "expr",
    "express",
    "expressway",
    "expw",
    "expy",
    "ext",
    "extension",
    "extensions",
    "extn",
    "extnsn",
    "exts",
    "fall",
    "falls",
    "ferry",
    "field",
    "fields",
    "flat",
    "flats",
    "fld",
    "flds",
    "fls",
    "flt",
    "flts",
    "ford",
    "fords",
    "forest",
    "forests",
    "forg",
    "forge",
    "forges",
    "fork",
    "forks",
    "fort",
    "frd",
    "frds",
    "freeway",
    "freewy",
    "frg",
    "frgs",
    "frk",
    "frks",
    "frry",
    "frst",
    "frt",
    "frway",
    "frwy",
    "fry",
    "ft",
    "fwy",
    "garden",
    "gardens",
    "gardn",
    "gateway",
    "gatewy",
    "gatway",
    "gdn",
    "gdns",
    "glen",
    "glens",
    "gln",
    "glns",
    "grden",
    "grdn",
    "grdns",
    "green",
    "greens",
    "grn",
    "grns",
    "grov",
    "grove",
    "groves",
    "grv",
    "grvs",
    "gtway",
    "gtwy",
    "harb",
    "harbor",
    "harbors",
    "harbr",
    "haven",
    "havn",
    "hbr",
    "hbrs",
    "height",
    "heights",
    "hgts",
    "highway",
    "highwy",
    "hill",
    "hills",
    "hiway",
    "hiwy",
    "hl",
    "hllw",
    "hls",
    "hollow",
    "hollows",
    "holw",
    "holws",
    "hrbor",
    "ht",
    "hts",
    "hvn",
    "hway",
    "hwy",
    "inlet",
    "inlt",
    "is",
    "island",
    "islands",
    "isle",
    "isles",
    "islnd",
    "islnds",
    "iss",
    "jct",
    "jction",
    "jctn",
    "jctns",
    "jcts",
    "junction",
    "junctions",
    "junctn",
    "juncton",
    "key",
    "keys",
    "knl",
    "knls",
    "knol",
    "knoll",
    "knolls",
    "ky",
    "kys",
    "la",
    "lake",
    "lakes",
    "land",
    "landing",
    "lane",
    "lanes",
    "lck",
    "lcks",
    "ldg",
    "ldge",
    "lf",
    "lgt",
    "lgts",
    "light",
    "lights",
    "lk",
    "lks",
    "ln",
    "lndg",
    "lndng",
    "loaf",
    "lock",
    "locks",
    "lodg",
    "lodge",
    "loop",
    "loops",
    "lp",
    "mall",
    "manor",
    "manors",
    "mdw",
    "mdws",
    "meadow",
    "meadows",
    "medows",
    "mews",
    "mi",
    "mile",
    "mill",
    "mills",
    "mission",
    "missn",
    "ml",
    "mls",
    "mn",
    "mnr",
    "mnrs",
    "mnt",
    "mntain",
    "mntn",
    "mntns",
    "motorway",
    "mount",
    "mountain",
    "mountains",
    "mountin",
    "msn",
    "mssn",
    "mt",
    "mtin",
    "mtn",
    "mtns",
    "mtwy",
    "nck",
    "neck",
    "opas",
    "orch",
    "orchard",
    "orchrd",
    "oval",
    "overlook",
    "overpass",
    "ovl",
    "ovlk",
    "park",
    "parks",
    "parkway",
    "parkways",
    "parkwy",
    "pass",
    "passage",
    "path",
    "paths",
    "pike",
    "pikes",
    "pine",
    "pines",
    "pk",
    "pkway",
    "pkwy",
    "pkwys",
    "pky",
    "pl",
    "place",
    "plain",
    "plaines",
    "plains",
    "plaza",
    "pln",
    "plns",
    "plz",
    "plza",
    "pne",
    "pnes",
    "point",
    "points",
    "port",
    "ports",
    "pr",
    "prairie",
    "prarie",
    "prk",
    "prr",
    "prt",
    "prts",
    "psge",
    "pt",
    "pts",
    "pw",
    "pwy",
    "rad",
    "radial",
    "radiel",
    "radl",
    "ramp",
    "ranch",
    "ranches",
    "rapid",
    "rapids",
    "rd",
    "rdg",
    "rdge",
    "rdgs",
    "rds",
    "rest",
    "ri",
    "ridge",
    "ridges",
    "rise",
    "riv",
    "river",
    "rivr",
    "rn",
    "rnch",
    "rnchs",
    "road",
    "roads",
    "route",
    "row",
    "rpd",
    "rpds",
    "rst",
    "rte",
    "rue",
    "run",
    "rvr",
    "shl",
    "shls",
    "shoal",
    "shoals",
    "shoar",
    "shoars",
    "shore",
    "shores",
    "shr",
    "shrs",
    "skwy",
    "skyway",
    "smt",
    "spg",
    "spgs",
    "spng",
    "spngs",
    "spring",
    "springs",
    "sprng",
    "sprngs",
    "spur",
    "spurs",
    "sq",
    "sqr",
    "sqre",
    "sqrs",
    "sqs",
    "squ",
    "square",
    "squares",
    "st",
    "sta",
    "station",
    "statn",
    "stn",
    "str",
    "stra",
    "strav",
    "strave",
    "straven",
    "stravenue",
    "stravn",
    "stream",
    "street",
    "streets",
    "streme",
    "strm",
    "strt",
    "strvn",
    "strvnue",
    "sts",
    "sumit",
    "sumitt",
    "summit",
    "te",
    "ter",
    "terr",
    "terrace",
    "throughway",
    "tl",
    "tpk",
    "tpke",
    "tr",
    "trace",
    "traces",
    "track",
    "tracks",
    "trafficway",
    "trail",
    "trailer",
    "trails",
    "trak",
    "trce",
    "trfy",
    "trk",
    "trks",
    "trl",
    "trlr",
    "trlrs",
    "trls",
    "trnpk",
    "trpk",
    "trwy",
    "tunel",
    "tunl",
    "tunls",
    "tunnel",
    "tunnels",
    "tunnl",
    "turn",
    "turnpike",
    "turnpk",
    "un",
    "underpass",
    "union",
    "unions",
    "uns",
    "upas",
    "valley",
    "valleys",
    "vally",
    "vdct",
    "via",
    "viadct",
    "viaduct",
    "view",
    "views",
    "vill",
    "villag",
    "village",
    "villages",
    "ville",
    "villg",
    "villiage",
    "vis",
    "vist",
    "vista",
    "vl",
    "vlg",
    "vlgs",
    "vlly",
    "vly",
    "vlys",
    "vst",
    "vsta",
    "vw",
    "vws",
    "walk",
    "walks",
    "wall",
    "way",
    "ways",
    "well",
    "wells",
    "wl",
    "wls",
    "wy",
    "xc",
    "xg",
    "xing",
    "xrd",
    "xrds",
}


try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(MODEL_PATH)
except OSError:
    warnings.warn(
        "You must train the model (parserator train --trainfile "
        "FILES) to create the %s file before you can use the parse "
        "and tag methods" % MODEL_FILE
    )


def parse(address_string: str) -> list[tuple[str, str]]:
    tokens = tokenize(address_string)

    if not tokens:
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))


def tag(address_string: str, tag_mapping=None) -> tuple[dict[str, str], str]:
    tagged_components: dict[str, list] = {}

    last_label = None
    is_intersection = False
    og_labels = []

    for token, label in parse(address_string):
        if label == "IntersectionSeparator":
            is_intersection = True
        if "StreetName" in label and is_intersection:
            label = "Second" + label

        # saving old label
        og_labels.append(label)
        # map tag to a new tag if tag mapping is provided
        if tag_mapping and tag_mapping.get(label):
            label = tag_mapping.get(label)
        else:
            label = label

        if label == last_label:
            tagged_components[label].append(token)
        elif label not in tagged_components:
            tagged_components[label] = [token]
        else:
            raise RepeatedLabelError(address_string, parse(address_string), label)

        last_label = label

    tagged_address: dict[str, str] = {}
    for token in tagged_components:
        component = " ".join(tagged_components[token])
        component = component.strip(" ,;")
        tagged_address[token] = component

    if "AddressNumber" in og_labels and not is_intersection:
        address_type = "Street Address"
    elif is_intersection and "AddressNumber" not in og_labels:
        address_type = "Intersection"
    elif "USPSBoxID" in og_labels:
        address_type = "PO Box"
    else:
        address_type = "Ambiguous"

    return tagged_address, address_type


def tokenize(address_string: str) -> list[str]:
    if isinstance(address_string, bytes):
        address_string = str(address_string, encoding="utf-8")
    address_string = re.sub("(&#38;)|(&amp;)", "&", address_string)
    re_tokens = re.compile(
        r"""
    \(*\b[^\s,;#&()]+[.,;)\n]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                       # [^'#abc'] -> ['#']
    """,
        re.VERBOSE | re.UNICODE,
    )

    tokens = re_tokens.findall(address_string)

    if not tokens:
        return []

    return tokens


Feature = dict[str, typing.Union[str, bool, "Feature"]]


def tokenFeatures(token: str) -> Feature:
    if token in ("&", "#", "½"):
        token_clean = token
    else:
        token_clean = re.sub(r"(^[\W]*)|([^.\w]*$)", "", token, flags=re.UNICODE)

    token_abbrev = re.sub(r"[.]", "", token_clean.lower())
    features = {
        "abbrev": token_clean[-1] == ".",
        "digits": digits(token_clean),
        "word": (token_abbrev if not token_abbrev.isdigit() else False),
        "trailing.zeros": (
            trailingZeros(token_abbrev) if token_abbrev.isdigit() else False
        ),
        "length": (
            "d:" + str(len(token_abbrev))
            if token_abbrev.isdigit()
            else "w:" + str(len(token_abbrev))
        ),
        "endsinpunc": (
            token[-1] if bool(re.match(r".+[^.\w]", token, flags=re.UNICODE)) else False
        ),
        "directional": token_abbrev in DIRECTIONS,
        "street_name": token_abbrev in STREET_NAMES,
        "has.vowels": bool(set(token_abbrev[1:]) & set("aeiou")),
    }

    return features


def tokens2features(address: list[str]) -> list[Feature]:
    feature_sequence = [tokenFeatures(address[0])]
    previous_features = feature_sequence[-1].copy()

    for token in address[1:]:
        token_features = tokenFeatures(token)
        current_features = token_features.copy()

        feature_sequence[-1]["next"] = current_features
        token_features["previous"] = previous_features

        feature_sequence.append(token_features)

        previous_features = current_features

    feature_sequence[0]["address.start"] = True
    feature_sequence[-1]["address.end"] = True

    if len(feature_sequence) > 1:
        feature_sequence[1]["previous"]["address.start"] = True  # type: ignore [index]
        feature_sequence[-2]["next"]["address.end"] = True  # type: ignore [index]

    return feature_sequence


def digits(token: str) -> typing.Literal["all_digits", "some_digits", "no_digits"]:
    if token.isdigit():
        return "all_digits"
    elif set(token) & set(string.digits):
        return "some_digits"
    else:
        return "no_digits"


# for some reason mypy can't believe that this will return a str as of 10/2024
def trailingZeros(token):
    results = re.findall(r"(0+)$", token)
    if results:
        return results[0]
    else:
        return ""


class RepeatedLabelError(probableparsing.RepeatedLabelError):
    REPO_URL = "https://github.com/datamade/usaddress/issues/new"
    DOCS_URL = "https://usaddress.readthedocs.io/"
