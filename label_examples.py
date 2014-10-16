from usaddress import parse as parser
import parserator

labels = [
    ['not addr', 'Null'],
    ['addr #', 'AddressNumber'],
    ['st dir pre', 'StreetNamePreDirectional'],
    ['st dir post', 'StreetNamePostDirectional'],
    ['st name', 'StreetName'],
    ['st type post', 'StreetNamePostType'],
    ['st type pre', 'StreetNamePreType'],
    ['intersection separator', 'IntersectionSeparator'],
    ['unit type', 'OccupancyType'],
    ['unit no', 'OccupancyIdentifier'],
    ['box type', 'USPSBoxType'],
    ['box no', 'USPSBoxID'],
    ['city', 'PlaceName'],
    ['state', 'StateName'],
    ['zip', 'ZipCode'],
    ['landmark', 'LandmarkName'],
    ['box group type', 'USPSBoxGroupType'],
    ['box group id', 'USPSBoxGroupID'],
    ['address number prefix', 'AddressNumberPrefix'],
    ['address number suffix', 'AddressNumberSuffix'],
    ['subaddress id', 'SubaddressIdentifier'],
    ['subaddress type', 'SubaddressType'],
    ['recipient', 'Recipient'],
    ['streetname modifer, pre', 'StreetNamePreModifier'],
    ['building name', 'BuildingName'],
    ['corner/junction', 'CornerOf']

]

parserator.manual_labeling.xmlLabeler(labels, parser)
