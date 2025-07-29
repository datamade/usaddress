Training your own model
=======================

You can always install a stable version of usaddress from [the Python Package Index](https://pypi.python.org/pypi/usaddress) by running `pip install usaddress`. But what if you want to **train your own version** of the model to do things that the current release isn't capable of? By labelling and training your own data, you'll be able to:

1. parse addresses that aren't yet supported 
2. push usaddress beyond its limits 
3. help make this library work better for everyone

What are we doing?
--------

Creating a new model involves three core steps:

1. **Labeling** addresses – help the machine understand them
2. **Training** the model – let usaddress see patterns in the data 
3. **Testing** the model - make sure your changes made things better

Sound interesting? Let's look at the steps in more detail.

How it's done
-----

**0. Create a local version of the repo.**

The first step in contributing to any open-source project is to fork the repository. If this is your first time, GitHub has a [nice guide to forking and contributing](https://help.github.com/articles/fork-a-repo/) that you should take a look at. (We also encourage contributors to [make a separate branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) for their work, which makes things easier on our end.) When you've forked the repo and you're ready to roll, come back here to get started developing.

After forking the repo, you'll need to get usaddress running on your machine. Running the following commands in the command line will install the proper dependencies and initialize a development version of usaddress:

```
cd usaddress  
pip install setuptools
python setup.py develop  
parserator train training/labeled.xml usaddress 
```

If you run into problems building your own copy of usaddress, don't hesitate to [open an issue](https://github.com/datamade/usaddress/issues/new) and the DataMade team will help you get started.

**1. Collect the addresses that are making usaddress fail.**

Once you have a local version of usaddress up and running, you're ready to start collecting addresses.

For each pattern that fails, you'll want to collect a handful of examples to make into **training data.** These examples should correspond to real world addresses that make usaddress fail - it's important to make sure that you're not influencing usaddress with how you *think* addresses work, as opposed to how they *really* work. To get started collecting your examples, make a new CSV file in the `training/` directory. For this guide, we'll call the file `new_addresses.csv`.

Since usaddress is smart, it usually only needs 4-6 examples to understand any given pattern. Grab a few examples and copy the addresses to `training/new_addresses.csv`, separating each address with a new line:

```
training/new_addresses.csv
--------------------------

2822 HENRIETTA AVE HUNTINGDON VY PA 19006-8504
6625 HUNTINGDON PIKE HUNTINGDON VY PA 19006-8307
3555 HILLVIEW TURN HUNTINGDON VY PA 19006-2816
47 AMES CIR UNIT F4 HUNTINGDON VALLEY PA 19006-7976
```

(While CSV files are most often represented as spreadsheets, they're just plain text, so you can make them in any standard text editor. Just make sure to save your file with the .csv extension.)

Remember that CSV files interpret **commas** as delimiters between table cells. For usaddress to understand your addresses, each line needs to be only one cell. That means that if any of your addresses include commas, you'll need to encapsulate them in quotes:

```
training/new_addresses.csv
--------------------------

"JASON BOURNE, 123 MAIN ST, HUNTINGDON VY PA 19006-8504"
```

For each pattern, you'll also want to make **testing data**. Whereas training data helps your model make new connections, testing data makes sure that your model is actually learning the patterns that you want it to learn (and isn't overriding patterns that it has already learned through past training data). Make a new CSV file in the directory `measure_performance/testing data/` - we'll call the file `new_tests.csv` - and add an address or two for each new pattern you've identified:

```
measure_performance/testing_data/new_tests.csv
--------------------------------------------

1080 BUCK HILL DR HUNTINGDON VY PA 19006-7910
"Barack Obama, 1600 Pennsylvania Ave NW, Washington, DC 20500"
```

Resist the urge to make your testing data identical to your training data. For the most robust results, testing and training data should be **different instances of the same pattern.** This ensures that usaddress is learning to see new patterns in addresses, and not merely learning to regurgitate the information you've fed into it. 

**2. Label your addresses so that usaddress can understand them.**

Unfortunately, usaddress doesn't read text the same way that humans do. It needs to have **labeled data** to help it make sense of the address patterns you're feeding into it. For our training format, we use XML tagged strings corresponding to the [United States Thoroughfare, Landmark, and Postal Address Data Standard](http://www.urisa.org/advocacy/united-states-thoroughfare-landmark-and-postal-address-data-standard/). 

After it's been labeled, training data looks something like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <AddressCollection>
    <AddressString> <PlaceName>Soldotna</PlaceName> , <StateName>AK</StateName> <ZipCode>996699</ZipCode> </AddressString> 
    <AddressString> <AddressNumber>9112</AddressNumber> <StreetName>Mendenhall</StreetName> <StreetName>Mall</StreetName> <StreetNamePostType>Road</StreetNamePostType> , <PlaceName>Juneau</PlaceName> , <StateName>AK</StateName> <ZipCode>99801</ZipCode> </AddressString> 
    <AddressString> <USPSBoxType>Box</USPSBoxType> # <USPSBoxID>63</USPSBoxID> , <PlaceName>Cardova</PlaceName> , <StateName>AK</StateName> <ZipCode>99574</ZipCode> </AddressString> 
    <AddressString> <AddressNumberPrefix>32</AddressNumberPrefix> - <AddressNumber>233</AddressNumber> <StreetName>M</StreetName> <StreetNamePostType>Street</StreetNamePostType> , <PlaceName>Elmendorf</PlaceName> <PlaceName>Afb</PlaceName> , <StateName>AK</StateName> <ZipCode>99506</ZipCode> </AddressString> 
    <AddressString><StreetName>Ridgecrest</StreetName> <StreetNamePostType>Drive</StreetNamePostType> , <PlaceName>Bethel</PlaceName> , <StateName>AK</StateName> <ZipCode>99559</ZipCode> </AddressString>
    <AddressString> <AddressNumber>123</AddressNumber> <StreetNamePreDirectional>E.</StreetNamePreDirectional> <StreetName>Main</StreetName> <StreetNamePostType>Road</StreetNamePostType> , <OccupancyType>Suite</OccupancyType> <OccupancyIdentifier>A.</OccupancyIdentifier> , <PlaceName>Juneau</PlaceName> , <StateName>AK</StateName> <ZipCode>99801</ZipCode> </AddressString> 
  </AddressCollection>
```

Thankfully, you don't have to write this code by hand! This repo comes with a built-in labelling program to help you generate tagged XML strings quickly and easily. The labelling program runs in the command line, and you can start it with the following command:

```
parserator label <filepath for your input CSV> <filepath for your output XML> usaddress
```

The **output** filepath can be anything you want, since usaddress will make a new file with the name and location described by the path, but it's good practice to give it a similar name and location as the input CSV file. For our example, the command for labeling our training data will look like this:

```
parserator label training/new_addresses.csv training/new_addresses.xml usaddress
```

Run this command and the labeling program will launch in the command line. It will start by printing some information to describe the commands that you can use to label addresses:

```
Start console labeling!

**************************************************
These are the tags available for labeling:
0 : AddressNumberPrefix
1 : AddressNumber
2 : AddressNumberSuffix
3 : StreetNamePreModifier
4 : StreetNamePreDirectional
5 : StreetNamePreType
6 : StreetName
7 : StreetNamePostType
8 : StreetNamePostDirectional
9 : SubaddressType
10 : SubaddressIdentifier
11 : BuildingName
12 : OccupancyType
13 : OccupancyIdentifier
14 : CornerOf
15 : LandmarkName
16 : PlaceName
17 : StateName
18 : ZipCode
19 : USPSBoxType
20 : USPSBoxID
21 : USPSBoxGroupType
22 : USPSBoxGroupID
23 : IntersectionSeparator
24 : Recipient
25 : NotAddress

type 'help' at any time to see labels
type 'oops' if you make a labeling error

**************************************************
```

During the labeling process, the program will ask you to match portions of the address to the **tags** that you can see above. Tagging an address is like diagramming a sentence: it breaks down the address into its smallest components and describes how each part relates to the whole.

Our tagging standard can take some time to get used to if you're not familiar with it. If you're confused about how to tag certain parts of an address, [follow the short guidelines in our documentation](http://usaddress.readthedocs.io/en/latest/#details) or consult the [official data standard](http://www.urisa.org/clientuploads/directory/GMI/Professional%20Practice/Address%20Standard/AddressStandard_Approved_Apr11_02Content.pdf). For more complicated questions, feel free to [open an issue in this repo](https://github.com/datamade/usaddress/issues/new) and the DataMade team can weigh in on your problem. 

After the instructions print, the program will begin prompting you to label addresses. Each prompt starts by using the current model to make an educated guess about the proper labels:

```
--------------------------------------------------
STRING: 2822 HENRIETTA AVE HUNTINGDON VY PA 19006-8504
| 2822       | AddressNumber      |
| HENRIETTA  | StreetName         |
| AVE        | StreetNamePostType |
| HUNTINGDON | PlaceName          |
| VY         | StateName          |
| PA         | StateName          |
| 19006-8504 | ZipCode            |
Is this correct? (y)es / (n)o / (s)kip / (f)inish tagging / (h)elp
```

In this case, usaddress got this address mostly right, but mislabelled `VY` as a `StateName` instead of a `PlaceName`. Enter `n` to tell it that the labels aren't correct, and then enter `return` (or `enter`) to accept all of the labels up to `VY`:

```
--------------------------------------------------
STRING: 2822 HENRIETTA AVE HUNTINGDON VY PA 19006-8504
| 2822       | AddressNumber      |
| HENRIETTA  | StreetName         |
| AVE        | StreetNamePostType |
| HUNTINGDON | PlaceName          |
| VY         | StateName          |
| PA         | StateName          |
| 19006-8504 | ZipCode            |
Is this correct? (y)es / (n)o / (s)kip / (f)inish tagging / (h)elp
n
What is '2822' ? If AddressNumber hit return
<return>
What is 'HENRIETTA' ? If StreetName hit return
<return>
What is 'AVE' ? If StreetNamePostType hit return
<return>
What is 'HUNTINGDON' ? If PlaceName hit return
<return>
What is 'VY' ? If StateName hit return
```

Based on the tag list above, we can see that `PlaceName` corresponds to the input `16` in the program. So add the appropriate label:

```
What is 'VY' ? If StateName hit return
16
```

Then accept the rest of the labels, since the model guessed them correctly:

```
What is 'PA' ? If StateName hit return
<return>
What is '19006-8504' ? If ZipCode hit return
<return>
```

Once you've evaluated every portion of the address, the program will move on to another example and the process will start over. 

Note that you can make use of helper commands to speed up the labeling process. If you decide that an address is not representative and you want to skip it, you can enter `s`; or if you want to quit labeling entirely, you can enter `f` and the program will stop, saving your progress in a secondary file. If you make a mistake during the labeling process itself, you can always enter `oops` to restart the labelling of the current address or `help` to see a list of possible labels.

After the program has prompted you to label every address, navigate to the target directory that you specified and confirm that a new XML file has been created (in this case, `training/new_addresses.xml`). 

**3. Train the model.**

So you've got a labeled XML file for our training data. Great! Now it's time to use it to teach the model to parse new patterns.

The training command for usaddress follows the following format:

```
parserator train <training data> usaddress
```

For stable releases, the DataMade team collects canonical training data in the file `training/labeled.xml`. Recall that when you initialized usaddress on your machine, you ran the command like this:

```
parserator train training/labeled.xml usaddress
```

But usaddress can also accept *multiple* files to use as training data. As you develop a new model, you should enforce separation between new and canonical training data to make debugging easier. So you can feed the model both files as input, separated by a comma:

```
parserator train training/labeled.xml,training/new_addresses.xml usaddress
```

After running the command, you should see output that looks something like this:

```
renaming old model: usaddress/usaddr.crfsuite -> usaddress/usaddr_2016_12_19_21286.crfsuite

training model on 1359 training examples from ['training/labeled.xml', 'trainingnew_addresses.xml']

done training! model file created: usaddress/usaddr.crfsuite
```

This output confirms that usaddress has learned from the new training data. Nice!

**4. Test the model.**

It's certainly exciting to know that you've added new training data to usaddress and changed the model, but it won't be very helpful unless we can verify that parsing behavior has actually *improved* based on the changes. To do that, you can check the model against a set of **testing data**.

Recall that you set aside a small portion of your addresses for testing in the CSV file `measure_performance/test_data/new_tests.csv`. Now that usaddress has (hopefully) learned to parse your new patterns, you can spot check it by labeling the testing data:

```
parserator label measure_performance/test_data/new_tests.csv measure_performance/test_data/new_tests.xml usaddress
```

The labeling program will launch, and if usaddress can suggest the proper labels for your testing data, you'll know that it has correctly learned the patterns you identified. (If, on the other hand, usaddress seems to fail on those patterns, you'll have to go back and add more examples of that pattern to your training data and retrain the model following steps 2 and 3.)

But it's not good enough to confirm that usaddress has learned new patterns – you also need to confirm that it hasn't *unlearned* old patterns in the process of incorporating your new training data. To do that, run the usaddress testing suite with the following command:

```
pytest
```

The output will fill your screen with a big block of dots (.) and/or Fs (F). Each dot corresponds to a test that *passed* (meaning that usaddress produced the expected parse for an address) while each F corresponds to a test that *failed* (meaning that usaddress failed to properly parse the address). 

If all the tests passed, look below the results block and you'll see a short confirmation output:

```
--------------------------------
Ran 4896 tests in 2.158s

OK
```

Congratulations! The model has officially improved. You can safely move on to step 5b, where you'll get your work ready to be shared.

If any of our tests failed, however, things become more complicated. The output will break down the tests that failed, showing you the parse that the model produced (labeled `pred`) and the parse that the test expected (labeled `true`). In this case, jump to step 5a to debug your errors.

If you'd like to additionally spot check singular addresses in the python shell, install a virtual environment, activate it, install your WIP version of this package, and open a shell.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]" -v
python
# shell starts up
>>> 
```

Then import usaddress and start parsing!
```python
>>> import usaddress
>>> usaddress.parse("a funky address")
```

**5a. Repeat steps 1-4 until the tests pass.**

If you've arrived at this step, it means that some of your tests failed. Uh oh! 

To cut a new release of usaddress, all canonical tests need to pass. That means before sharing your work, you'll have to go back and retrain the model to properly parse the addresses that it's failing on.

Take the failing addresses and try to find real-world addresses that match the pattern. Mapping software like [Open Street Map](http://www.openstreetmap.org/#map=5/51.500/-0.100) and [Google Maps](https://www.google.com/maps) can be helpful for searching for similar address patterns. Collect new addresses and repeat steps 1-4 until all of the tests in the testing suite pass.

Once all of the tests are passing, you're safe to move on to step 5b.

**5b. Add your training and testing data.**

If you've arrived at this step, it means that all of your new and old tests passed and your model is good to go. Fantastic! Next up in order to have the public package trained and tested on your data, you'll need to add it to the canonical data.

To do this, just copy your everything within the `<AddressCollection>` tags of your `new_addresses.xml` file, and paste it towards the end of the same tags within the `labeled.xml` file found in the `training/` directory. Repeat the same steps for the testing data and the `test_data/` directory.

**5c. Make a pull request.**

Now it's time to share your work. GitHub provides a powerful way of sharing code through the *pull request* feature (and has a [really nice guide](https://help.github.com/articles/creating-a-pull-request/) for first-timers explaining how it works). Open up a new pull request and give us a short description of what you changed: What address patterns did you fix? Where did you store your training data? How many new examples/tests did you add? The clearer your description of your work, the easier it will be for the DataMade team to determine whether it's ready to go.

If you made it this far, **great job!** We appreciate your dedication to making usaddress better for the whole community. Drop us a line on [GitHub](https://github.com/datamade) or on [Twitter](https://twitter.com/DataMadeCo) and let us know how you're using usaddress.

Need help?
----------

We want contributing to usaddress to be as painless as possible. If you run into problems following any of our documentation, feel free to [open an issue](https://github.com/datamade/usaddress/issues/new) describing your problem and the DataMade team would be glad to help.
