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
as published by Sam Hocevar. See the COPYING file for more details.

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
for idx in range(num_checks):
    rndfile = random.choice(allfiles)
    file_one = open(os.path.join(first_path, rndfile), 'rb')
    file_two = open(os.path.join(second_path, rndfile), 'rb')
    while True:
        data_one = file_one.read(128)
        data_two = file_two.read(128)
        if not data_one:
            break
        hash_one = hashlib.md5(data_one).hexdigest()
        hash_two = hashlib.md5(data_two).hexdigest()
        if hash_one != hash_two:
            print("MD5 mismatch in file pair: %s - %s" % (
                                    file_one.name, file_two.name))
            continue
    print("Success: File %s matches %s" % (file_one.name, file_two.name))
    print("\n-----------\n")



