import pycrfsuite


file = open('./training_data/us50.train.tagged', 'r')
lines = file.readlines()

addr_training = [[]]

addr_index = 0
token_index = 0

tag_list = ['', 'street number', '2', 'street', '4', 'city', 'state', 'zip']

for line in lines:
	if line == '\n':
		addr_index += 1
		token_index = 0
		addr_training.append([])
	else:
		split = line.split(' |')
		token_string = split[0]
		token_num = split[1].rstrip()
		token_num = int(token_num)
		token_tag = tag_list[token_num]
		addr_training[addr_index].append((token_string, token_tag))

print addr_training #test


def word2features(address, i):
	word = address[i][0]
	features = ['word.lower=' + word.lower(), 'word.isdigit=%s' % word.isdigit()]
	return features

def addr2features(address):
	return [word2features(address, i) for i in range(len(address))]

def addr2labels(address):
	return [address[i][1] for i in range(len(address))]


#print addr2features(addr_training[0]) #test
#print addr2labels(addr_training[0]) #test


x_train = [addr2features(addr) for addr in addr_training]
y_train = [addr2labels(addr) for addr in addr_training]

#print zip(x_train, y_train) #test

trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(x_train, y_train):
	trainer.append(xseq, yseq)