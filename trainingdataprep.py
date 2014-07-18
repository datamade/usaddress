import pycrfsuite

def parseLines(lines):
	parsed = [[]]
	addr_index = 0
	token_index = 0
	tag_list = ['', 'street number', '2', 'street', '4', 'city', 'state', 'zip']

	for line in lines:
		if line == '\n':
			addr_index += 1
			token_index = 0
			parsed.append([])
		else:
			split = line.split(' |')
			token_string = split[0]
			token_num = split[1].rstrip()
			token_num = int(token_num)
			token_tag = tag_list[token_num]
			parsed[addr_index].append((token_string, token_tag))
	return parsed

def word2features(address, i):
	word = address[i][0]
	features = ['word.lower=' + word.lower(), 'word.isdigit=%s' % word.isdigit()]
	return features

def addr2features(address):
	return [word2features(address, i) for i in range(len(address))]

def addr2labels(address):
	return [address[i][1] for i in range(len(address))]


# prep the training & test data
file = open('./training_data/us50.train.tagged', 'r')
train_lines = file.readlines()
train_data = parseLines(train_lines)

x_train = [addr2features(addr) for addr in train_data]
y_train = [addr2labels(addr) for addr in train_data]

file = open('./training_data/us50.test.tagged', 'r')
test_lines = file.readlines()
test_data = parseLines(test_lines)

x_test = [addr2features(addr) for addr in test_data]
y_test = [addr2labels(addr) for addr in test_data]


#train model
trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(x_train, y_train):
	trainer.append(xseq, yseq)