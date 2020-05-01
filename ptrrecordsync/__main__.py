#!/usr/bin/python3

#
# by Dennis Cole III <dennis@lbsys.xyz>
#
# This script will take a list of A records from a BIND9 zonefile and create PTR records via nsupdate...
# ...fun
# IPv6 is not considered for this
#

import argparse
import string
import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def valid_file(file):
    if not os.path.isfile(file):
        print('The file {f} could not be found...'.format(f=file))
        exit(1)
    return file

parser = argparse.ArgumentParser(description='PTR Record Sync')


parser.add_argument('zonefile', type=valid_file,
    help='Location of the zone file to be processed. This is required.')
parser.add_argument('keyfile', type=valid_file,
    help='Location of the tsig key file. This is required.')

def process_check(**kwargs):
    '''Checking for process in Linux'''
    process = kwargs.get('process')
    try:
        subprocess.run(['which', process], stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError as err:
        print('{proc} is required to continue. Please install.'.format(
            proc=process))
        exit(1)

def nsupdate_cmd(**kwargs):
    '''Runs nsupdate command'''
    command = kwargs.get('command')
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()

def main():
    args = parser.parse_args()
    zonefile = args.zonefile
    keyfile = args.keyfile
    rndcprocess = 'rndc'
    nsupdateprocess = 'nsupdate'

    process_check(process=rndcprocess)
    process_check(process=nsupdateprocess)

    isgoodarecord = False
    ttl = '3600'
    arecordlist = []

    with open(zonefile) as forwardzone:
        for line in forwardzone:
            # I'm trying to find A records with a certain TTL specified above.
            # I'd also like to have my domain name, so that's what I'm trying to
            # do with this code
            if 'ORIGIN' in line:
                domainname = line.split()[1]
                # yes, the $ORIGIN line may appear more than once,
                # but my zone file just has two, the first being root,
                # second being my zone. Here's to cheating!!
            if 'TTL' in line:
                if ttl in line:
                    isgoodarecord = True
                else:
                    isgoodarecord = False
            if isgoodarecord and 'A' in line and not 'AAAA' in line:
                # Wrap it up and give to a baby on XMas because we're done
                arecordlist.append(line.split())

    for record in arecordlist:
        # Let's parse the list of A records so send to nsupdate
        hostname = record[0]
        ip = record[2]
        octets = ip.split('.')
        ptrrecord = '{oct4}.{oct3}.{oct2}.{oct1}.in-addr.arpa'.format(
            oct1=octets[0], oct2=octets[1], oct3=octets[2], oct4=octets[3])
        delptrrecord = 'update delete {ptr} IN PTR'.format(ptr=ptrrecord)
        updateptrrecord = 'update add {ptr} {t} IN PTR {hn}.{dn}'.format(
            ptr=ptrrecord, t=ttl, hn=hostname, dn=domainname)
        updatecommand = '{delptr}\n{upgptr}\nsend\nshow\nquit'.format(
            delptr=delptrrecord, upgptr = updateptrrecord)
        command = 'nsupdate -k {k} -v << EOF\n{command}\nEOF\n'.format(
            k=keyfile, command=updatecommand)

        nsupdate_cmd(command=command)

    # This below is not necessary, but my wife says I have to clean my room
    process = subprocess.Popen(
        'rndc sync -clean', stdout=subprocess.PIPE, shell=True)

if __name__ == '__main__':
    main()
