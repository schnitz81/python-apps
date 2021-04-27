import argparse
import socket
import datetime
import time

LOGFILE="/tmp/nwlogger.log"
STATUSTABLE = {}
INTERVAL = 2

def initialize_statustable(iplist,portlist):
    #create list for error handling
    for ip in iplist:
        STATUSTABLE[ip] = {}
        for port in portlist:
            STATUSTABLE[ip][port] = 0

def porttest(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((str(ip), int(port)))
    s.close()
    if result:
        return 1
    else:
        return 0

def main():

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest='iplist', action='append', required=True, help="Add IP to check")
    parser.add_argument('-p', '--port', dest='portlist', action='append', required=True, help="Add port to check")
    args = parser.parse_args()

    # get IPs and ports
    iplist = args.iplist
    portlist = args.portlist

    # Create status table and set zero as default state
    initialize_statustable(iplist,portlist)

    log(f"Started monitoring.  IPs: {iplist}  Ports: {portlist}")


    # infinite loop
    while True:

        # iterate through IPs and ports and run socket test
        for ip in iplist:
            for port in portlist:
                # print(f"ip:{ip} port:{port}")

                # get result from socket test
                result = porttest(ip,port)

                # compare to status table and log if status is changed
                if STATUSTABLE[ip][port] is not result and result == 1:
                    STATUSTABLE[ip][port] = 1
                    log(f"{ip} : {port} - connection lost")
                elif STATUSTABLE[ip][port] is not result and result == 0:
                    STATUSTABLE[ip][port] = 0
                    log(f"{ip} : {port} - connection established")
        time.sleep(INTERVAL)

def log(msg):
    try:
        with open(LOGFILE, 'a', encoding='utf-8') as fout:
            print(f"{datetime.datetime.now()} {msg}")
            fout.write(f"{datetime.datetime.now()} ")
            fout.write(msg)
            fout.write('\n')
    except Exception as le:
        print(f"Log file read error: {le}")

if __name__ == '__main__':
    main()
