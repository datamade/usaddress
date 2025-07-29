---
name: Improve Parser
about: Is a parse not looking the way you expected? Let us know here!
title: ''
labels: bad parse
assignees: ''

---

**The Input Address**
What string are you having an issue with?

(ex. 123 Main St. Chicago, Illinois)

**Current Output**
What is the parser currently returning?

123 - AddressNumber
Main - AddressNumber
St. - StreetNamePostType
Chicago - PlaceName
Illinois - PlaceName

**Expected Ouput**
What are you expecting the parser to return?

123 - AddressNumber
Main - StreetName
St. - StreetNamePostType
Chicago - PlaceName
Illinois - StateName

**Examples**
Preferably 8-12 real world examples with a similar pattern that we can use to train the parser. This can be from your dataset if you're comfortable sharing some.
- 456 Second St. Chicago, Illinois

**Additional context**
Optional. Add any other context here.
