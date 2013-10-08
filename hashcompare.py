"""
Compares files at random from two paths using md5.
Usage:
    python hashcompare.py <dir1> <dir2> <n>

    where <dir1> and <dir2> are the roots of the directory trees to compare
    and <n> is the number of files to compare (random selection).


License and copying

Copyright © 2014 Achilleas Koutsou
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the LICENSE file for more details.

"""

import sys
import os
import random
import hashlib

first_path = sys.argv[1]
second_path = sys.argv[2]
num_checks = int(sys.argv[3])

print("Building file list ...")
#allfiles = [os.path.join(path.replace(first_path, "", 1), filename)
#         for path, dirs, files in os.walk(first_path)
#         for filename in files]

allfiles = []
for path, dirs, files in os.walk(first_path):
    for filename in files:
        allfiles.append(os.path.join(path.replace(first_path+"/", "", 1), filename))
        sys.stdout.write("%i ...\r" % (len(allfiles)))
        sys.stdout.flush()



print("Comparing %i files at random ..." % num_checks)
successcount = 0
failcount = 0
for idx in range(num_checks):
    rndfile = random.choice(allfiles)
    try:
        file_one = open(os.path.join(first_path, rndfile), 'rb')
    except:
        sys.stderr.write("Error opening file %s\n" % (file_one))
        raise
    try:
        file_two = open(os.path.join(second_path, rndfile), 'rb')
    except:
        sys.stderr.write("Error opening file %s\n" % (file_two))
        raise
    while True:
        try:
            data_one = file_one.read(128)
        except:
            sys.stdderr.write("Error reading file %s" % (file_one))
            raise
        try:
            data_two = file_two.read(128)
        except:
            sys.stdderr.write("Error reading file %s" % (file_two))
            raise
        if not data_one:
            break
        hash_one = hashlib.md5(data_one).hexdigest()
        hash_two = hashlib.md5(data_two).hexdigest()
        if hash_one != hash_two:
            print("\n%i/%i: MD5 mismatch in file pair: %s - %s" % (
                                    idx+1, num_checks,
                                    file_one.name, file_two.name))
            failcount += 1
            continue
    print("\n%i/%i: Success: File %s matches %s" % (
                        idx+1, num_checks,
                        file_one.name, file_two.name))
    print("\n-----------")
    successcount += 1

print("\nDone!")
print("%i out of %i files checked matched (%i mismatches)" % (
                    successcount, num_checks, failcount))




