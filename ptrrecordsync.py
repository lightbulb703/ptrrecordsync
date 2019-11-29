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

parser = argparse.ArgumentParser()
parser.add_argument("zonefile", help="Location of the zone file to be processed")
parser.add_argument("keyfile", help="Location of the tsig key file")
args = parser.parse_args()
zonefile = args.zonefile
keyfile = args.keyfile
rndcprocess = "rndc"
nsupdateprocess = "nsupdate"

def nsupdate_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()

def main (zonefile,keyfile,rndcprocess,nsupdateprocess):
    isgoodarecord = False
    ttl = "3600"
    arecordlist = []

    with open(zonefile) as forwardzone:
        for line in forwardzone:
            # I'm trying to find A records with a certain TTL specified above. I'd also like to have my domain name, so that's what I'm trying to do with this code
            if "ORIGIN" in line:
                domainname = line.split()[1]
                # yes, the $ORIGIN line may appear more than once, but my zone file just has two, the first being root, second being my zone. Here's to cheating!!
            if "TTL" in line:
                if ttl in line:
                    isgoodarecord = True
                else:
                    isgoodarecord = False
            if isgoodarecord and "A" in line and not "AAAA" in line:
                # Wrap it up and give to a baby on XMas because we're done
                arecordlist.append(line.split())                

    for record in arecordlist:
        # Let's parse the list of A records so send to nsupdate
        hostname = record[0]
        ip = record[2]
        octets = ip.split(".")
        ptrrecord = f"{octets[3]}.{octets[2]}.{octets[1]}.{octets[0]}.in-addr.arpa"
        delptrrecord = f"update delete {ptrrecord} IN PTR"
        updateptrrecord = f"update add {ptrrecord} {ttl} IN PTR {hostname}.{domainname}"
        updatecommand = f"{delptrrecord}\n{updateptrrecord}\nsend\nshow\nquit"
        command = "nsupdate -k {0} -v << EOF\n{1}\nEOF\n".format(keyfile, updatecommand)

        nsupdate_cmd(command)

    # This below is not necessary, but my wife says I have to clean my room
    process = subprocess.Popen("rndc sync -clean",stdout=subprocess.PIPE, shell=True)

if __name__ == '__main__':
    main(zonefile,keyfile,rndcprocess,nsupdateprocess)
