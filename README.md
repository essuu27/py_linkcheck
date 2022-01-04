# Introduction
py_linkchecker takes a long list of URLs and checks them to make sure that they are still valid and available.

# Setup
To use this script you will need three things:
- a mysql database
- a configuration file that holds the access details for the database, my.ini
- the script itself, py_linkcheck.py

## The mysql database
This script uses a mysql database to supply the list of URLs to be checked. It also uses the database as a transaction-state register. The transaction-state register is meant to 
keep track of which URLs have been processed, are yet to be processed and what the results 
are from URLs that have been processed.

Each row in the database should have the following format:

| ID  | URL  | Results  | Date  |
|---|---|---|---|

where
- ID is an integer, is set to autoincrement and is marked as the primary key. This ID is used internally by the script to keep track of URLs it is processing.
- URL is set as varchar(512). This is probably a bit long but this field is meant to hold the text representation of the URL to be checked
- Result is set as int(11) and records the numeric return code of a call to the related URL
- Date is set as datetime. If possible it should be setup with the following trigger: ON UPDATE CURRENT_TIMESTAMP . This column is meant as a record for the user to check when and if a URL has been checked. It is not used within the script and is not necessary to the function of the script.

Once you have the database setup you should import URLs into the database. The script is designed to use secure HTTP calls by default. As such you do not have to specify the protocol of a URL unless you require a unsecured connection to the resource. A URL list could look something like this:

```
https://www.someplace.abc
subsite.someplace.els
http://subsite2.anotherplac.abc
```

The first two URLs will be accessed via the secure protocol, the third URL by the unsecured protocol.

## The my.ini configuration file
A blank my.ini configuration file is included with this distribution. You should fill in 
the entries as necessary with the details needed to access your database. The entries should be self-explanatory.

If you are running this script on a multiuser access system then it is strongly suggested that you secure this file to prevent other users gaining access to your database. To do this you should typpe the following:

```
chown <myuser> my.ini
chmod 0600 my.ini
```

substituting '<myuser>' for the username of the account that will be running the script.

## The py_linkcheck.py script
Before running the script there are a couple of configuration tweaks you may wish to make. The first is the setting which controls the number of simultaneous URL checks that the script can make.

There is a variable named 'workers' on line 83. This is an integer variable and its value sets the number of concurrent web accesses the script should make. The higher this value is the more number of web agents the script will use. There are however limitations on the amount of web agents that the script can support. The number of web agents that the script can run concurrently is limited by factors such as network bandwidth, system memory and overall system load.

The 'workers' variable is also used when setting up the connection pool to the mysql database. By default a mysql database will support upto  a maximum of 
32 concurrent connections. You will need to contact your DBA to find out what limits may be applied to your database.

