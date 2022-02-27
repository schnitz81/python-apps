import argparse
from os.path import exists
import sys
import subprocess


# https://docs.min.io/docs/python-client-quickstart-guide.html

TESTFILE = "test.txt"
ALIASNAME = "testingalias"
TESTBUCKETNAME = "testbucket1337"

def check_minio_client():
    if not exists('mc'):
        print("Error: Minio client not found.")
        sys.exit(1)

def argument_parser():
    parser = argparse.ArgumentParser(prog='minio-functiontest', usage='%(prog)s (server URL) (access_key) (secret_key)')
    parser.add_argument('server', type=str, nargs='+')
    parser.add_argument('access_key', type=str, nargs='+')
    parser.add_argument('secret_key', type=str, nargs='+')
    parser.add_argument("-p", "--port", action='store', dest="port", type=int,
                        help="Port for the minio API (if not standard 9000).", nargs='?')
    args = parser.parse_args()
    return args

def create_testfile():
    try:
        with open(TESTFILE, 'w', encoding='utf-8') as fout:
            fout.write("testfile content")
    except Exception as filewriteerror:
        print(f"Value file read error: {filewriteerror}")

def execute(command):
    try:
        value = subprocess.run(f'''
                {command}
            ''',
            shell=True, check=True,
            executable='/bin/bash',
            capture_output=True,
            text=True)
        return value.stdout
    except Exception as execute_e:
        print(execute_e)

def main():

    # Check minio client availability
    check_minio_client()

    args = argument_parser()
    server = args.server[0]
    access_key = args.access_key[0]
    secret_key = args.secret_key[0]
    port = args.port

    # if http is included in input parameters
    if "http" in server:
        print("Error: Don't include http in server input parameter")
        sys.exit(1)

    # use default port number if it's not specified
    if port is None:
        port = 9000

    print(server)
    print(access_key)
    print(secret_key)
    print(port)

    # create a test file to upload
    create_testfile()

    # create alias
    print("\nCreating alias for minio server.")
    cmdoutput = execute(f"./mc alias set {ALIASNAME} http://{server}:{port} {access_key} {secret_key}")
    print(cmdoutput)

    # check if alias was created successfully
    print("\nChecking alias existence.")
    cmdoutput = execute(f"./mc alias list {ALIASNAME} | xargs")
    if ALIASNAME not in cmdoutput:
        print("FAILED: alias not created. Check login, port and connectivity.")
        sys.exit(1)

    # create bucket
    print("\nCreating test bucket...")
    cmdoutput = execute(f"./mc mb {ALIASNAME}/{TESTBUCKETNAME}")
    print(cmdoutput)

    # upload local file to bucket in minio
    print("Uploading test file...")
    cmdoutput = execute(f"./mc cp test.txt {ALIASNAME}/{TESTBUCKETNAME}")
    print(cmdoutput)

    print("\nChecking test file availability.")
    cmdoutput = execute(f"./mc ls {ALIASNAME}/{TESTBUCKETNAME}")
    print(cmdoutput)

    # store result
    if cmdoutput is not None:
        if "test.txt" in cmdoutput:
            success = True
        else:
            success = False
    else:
        success = False

    print("\nCleaning up minio storage from test objects...")
    cmdoutput = execute(f"./mc rm {ALIASNAME}/{TESTBUCKETNAME}/test.txt")
    print(cmdoutput)
    cmdoutput = execute(f"./mc rb {ALIASNAME}/{TESTBUCKETNAME}")
    print(cmdoutput)

    # print test result
    if success:
        print("*** SUCCESS: Test file found in bucket. ***")
        sys.exit(0)
    else:
        print("*** FAILED: Unable to find testfile in bucket. ***")
        sys.exit(1)


if __name__ == '__main__':
    main()
