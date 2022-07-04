# Myles Dear's Radix DLT interview submission (Jun 23, 2022)

## Environment setup
This solution is tested on Ubuntu 20.04.4 LTS using python3.8.

Update the package index:

`sudo apt-get update`

Install libpython3.8 deb package:

`sudo apt-get install libpython3.8`

Change to a directory you want to contain your Python virtual environment.
Substitute `/path/to/venv/parent/dir` with the appropriate local directory path.

`cd /path/to/venv/parent/dir; python3.8 -m venv mdear_submission; cd mdear_submission; source bin/activate`

Install requirements (located in my git repository)

`pip install -r requirements.txt`

Examples given in bash.  Add the following commands to `~/.bashrc`:

Set an environment variable that locates the directory where the jar file
of the server under test is located.  Replace `/path/to/` with the appropriate path name:

`export MERKLE_FILE_SERVER_ROOT=/path/to/radix-merkle-file-server-sdet-challenge`

Server output is written into a date/time stamped temporary directory

`$MERKLE_FILE_SERVER_LOGS/merkle_server_console*.log`.

Set an environment variable denoting where server output is to be written
(defaults to `/tmp` if not specified):

`export MERKLE_FILE_SERVER_LOGS=/tmp`

Then, apply:
`source ~/.bashrc`


## How to run unit tests
I have written unit tests to provite light coverage of sunny day usage of
the Merkle validation test automation framework, and black box automated
tests to cover light sunny day execution of server file retrieval and validation.

Ensure you have executed all commands in the environment setup section.
Clone this repo into a directory outside the venv directory.
cd into this repo's top level directory.
Type:

`python -m unittest .`

## Test plan

Category 1 : Sunny Day

    Test 1.1 Get entire test file icons_rgb_circle.png.  Validate contents against original.

    Test 1.2 Repeat test 1.1 but with a series of artifically 
    created test files of size 1K-1, 1K, 1K+1 and pseudorandom
    contents (to check for off
    by one errors).  Then move up to file sizes of 2K-1, 2K, 2K+1, and 
    cycle up from there in 1K increments all the way up to 100KB.


Category 2 : Rainy Day

    Test 2.1 Try corrupting a returned root hash, proof and piece contents and ensure validation
    fails as expectetd.


Category 3 : Scale/Stress Validation

    Test 3.1 : Large files
        Repeat test 1.1 but on artifically large test files 1K, 10K, 100K, 1MB, 10MB, 100MB, 1GB.
        Fill with pseudorandom patterns.
        Validate original file with reconstructed file and ensure binary equality.
        Note execution time and load factor during each test.  Determine if execution scales linearly or not based on file size.

    Test 3.2 : Multiple files
        Similar to 2.1 create a set of test files of multiple sizes.  Launch server specifying all these multiple files and test download of each file sequentially.
        Validate original file with reconstructed file and ensure binary equality.
        Characterize loading behavior as in test 2.1.

    Test 3.3: Multiple files
        Similar to 2.2 but retrieve each file in parallel, to the maximum number of connections supported by the server.  Find system limits/breaking points.  Characterize throughput, memory usage, storage
        usage.

    Test 3.4: DDOS attach
        Try to DDOS the server by sending rapid requests.

    Test 3.5: Soak test
        Set an automated test to continually run a file reconstruction / validation loop, checking for potential memory leaks.
        Monitor the resource consumption of the process during this long-term (ie. overnight) test.


    Category 4 : Fault Tolerance Validation
        Test 4.1 : Planned server restart/recovery 
            During the middle of a transfer, kill the server and restart it.  Wait for it to come up again.
            Resume the transfer and validate the resulting file.

        Test 4.2 : Unplanned server restart/recovery 
            Kill the server at a random/unexpected time during the recovery of file pieces and ensure the
            client fails gracefully and then re-requests the failing operation and ultimately validates the
            entire file.


    Category 5 : API testing

        Test 5.1 : Bad verbs
            Test the given hashes/piece APIs but use PUT, POST, PATCH and DELETE verbs, ensure these fail appropriately.

        Test 5.2 : pieces API : Bad hashid
            Provide unknown and badly formatted hashid, ensure graceful failure.

        Test 5.3 : pieces API : Bad index
            Provide out-of-bounds or non-numerical pieceIndex values, ensure these fail gracefully
            Reverse the hashId and pieceIndex in the URL and ensure
            failure.

        Test 5.4 : pieces API bad path
            Provide incomplete / unsupported path values on the GET URL, ensure graceful fail.
            For example, piece API without pieceIndex, or unsupport API such as "pieceZ".

        Test 5.5 : pieces API : missing required API elements
            Try getting a piece with a misformatted URL missing the
            hashId and/or the pieceIndex.

## Bug reports

## Suggestions to improve the exercise
1. The following link documents Merkle validations a little differently than the one used in 
your example, and may be good to integrate.
https://medium.com/crypto-0-nite/merkle-proofs-explained-6dd429623dc5

