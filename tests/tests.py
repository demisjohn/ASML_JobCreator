import os

results = []

for script, outputfile in [
    ("example01_multilayer_noalignments.py",
            "examplejob01_multilayer_noalignments.txt"),
    ("example02_alignment_and_imageslib.py",
            "examplejob02_alignments_and_imageslib.txt"),
        ]:

    # read the old file
    with open(outputfile, 'r') as inf:
        oldtext = inf.read()

    # change directory, make the new file, read, change directory
    os.chdir("..")
    os.system("python {}".format(script))
    with open(outputfile, 'r') as inf:
        newtext = inf.read()
    os.chdir("tests")

    if newtext == oldtext:
        results.append((script, "good"))
    else :
        results.append((script, "bad"))

print()
for script, result in results:
    if result == "good":
        print("{} is good!".format(script))
    else :
        print("{} fails the test!".format(script))

