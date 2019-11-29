# ptrrecordsync
From a BIND zone file, register PTR records

Scenario: You have a DHCP server that can register A record updates to your DNS server, but not PTR records.

That's why I created this script. I'm not a programmer by trade, so errors are possible.

Python3, Bind and Bind Utils are required. You can run this as a cron job or systemd timer.
