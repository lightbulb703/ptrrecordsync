# ptrrecordsync
#############################################
 From a BIND zone file, register PTR records
#############################################

Scenario: You have a DHCP server that can register A record updates to your
DNS server, but not PTR records.

That's why I created this script. I'm not a programmer by trade,
so errors are possible.

Python3, Bind and Bind Utils are required and I've only tested this on CentOS.

You can run this as a cron job or systemd timer (sample files provided for
systemd). The configuration file in /etc should have the zone file and key file
to run the update.

============
Installation
============

To install, use setup.py::

  python3 setup.py install

================
Running the sync
================

Usage::

  usage: ptrrecordsync.py [-h] [-z ZONEFILE] [-k KEYFILE]

  optional arguments:
    -h, --help            show this help message and exit
    -z ZONEFILE, --zonefile ZONEFILE
                          Location of the zone file to be processed. This is
                          required.
    -k KEYFILE, --keyfile KEYFILE
                          Location of the tsig key file. This is required.


The arguments above are actually required. Any collaboration, recommendations
would be great
