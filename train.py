import parserator

with open('training/training_data/labeled.xml') as example_file :
    parserator.train(example_file, 'usaddress/usaddr.crfsuite')
