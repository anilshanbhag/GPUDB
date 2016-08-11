# Used to run the SSB
# using GPUDB

import subprocess
import os

test_dir = "test/ssb_test/"
queries = ["q1_1.sql", "q1_2.sql", "q1_3.sql", "q2_1.sql", "q2_2.sql", "q2_3.sql", "q3_1.sql", "q3_2.sql", "q3_3.sql", "q3_4.sql", "q4_1.sql", "q4_2.sql", "q4_3.sql"]
schema_file = "ssb.schema"

def gen_data(sf):
    os.chdir("test/dbgen/")
    os.system("./dbgen -vfF -T a -s %d" % sf)
    os.chdir("../../src/utility/")
    os.system("make loader")
    os.system(" ./gpuDBLoader --lineorder ../../test/dbgen/lineorder.tbl --ddate ../../test/dbgen/date.tbl --customer ../../test/dbgen/customer.tbl --supplier ../../test/dbgen/supplier.tbl --part ../../test/dbgen/part.tbl")
    os.system("mkdir -p ../../data%d" % sf)
    os.system("mv LINEORDER* PART* CUSTOMER* SUPPLIER* DDATE* ../../data%d" % sf)

def gen_executables():
    global test_dir, queries, schema_file
    for query in queries:
        # Compile the query
        subprocess.call(["./translate.py", test_dir + query, test_dir + schema_file])
        os.chdir("src/cuda/")
        subprocess.call(["make", "gpudb"])
        subprocess.call(["cp", "GPUDATABASE", query.split('.')[0]])
        os.chdir("../../")

def run_executables(sf=1):
    os.chdir("src/cuda/")
    data_dir = "../../data%d/" % sf
    for query in queries:
        print "Running query " +  query
        subprocess.call(["./" + query.split('.')[0], "--datadir", data_dir])

if __name__ == "__main__":
    #gen_executables()
    run_executables(10)

