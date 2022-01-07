# Introduction
py_linkchecker takes a long list of URLs and checks them to make sure that they are still valid and available.

# Setup
The script uses two modules: concurrent.futures and mysql-connector-python. The concurrent.futures module is included in the standard installation of python from version 3.2.

The mysql-connector-python module needs to be installed. This can be done easily by opening a console/command prompt and typing:

`pip install mysql-connector-python`

When the mysql-connector-python module is installed your local installation of python should be able to provide the functionality needed by the script. You will then need to setup the following two things:

- a mysql database
- a configuration file that holds the access details for the database, my.ini

## The mysql database
You will need to setup a database to hold the URLs that you want checked. This database also records the results of any checks that are performed.

Each row in the database should have the following format:

| ID  | URL  | Results  | Date  |
|---|---|---|---|

where
- ID is an integer. It should be set as the *PRIMARY KEY*, and also should be set to autoincrement. This ID is used internally by the script as the 'unique ID' of each URL that is stored.
- URL is set as varchar(512). This is probably a bit long but this field is meant to hold the text representation of the URL to be checked
- Result is set as int(11) and records the numeric return code of a call to the related URL
- Date is set as a datetime variable. If possible it should be setup with the following trigger:

 ` ON UPDATE CURRENT_TIMESTAMP `

 This column records when a URL has been checked. It is not intended to be used within the script and is not necessary to the function of the script. It can be useful to monitor the progress of the script, though.

Once you have the database setup you should import URLs into the database. The script is designed to use secure HTTP protocol calls by default. As such you do not have to specify the protocol of a URL unless you require a unsecured connection to the resource. A URL list could look something like this:

```
https://www.someplace.abc
subsite.someplace.els
http://subsite2.anotherplac.abc
```

The first two URLs will be accessed via the secure protocol, the third URL by the unsecured protocol.

## The my.ini configuration file
A skeleton my.ini configuration file is included with this distribution. You should fill in the entries as necessary with the details needed to access your database. The entries should be self-explanatory.

If you are running this script on a multiuser access system then it is strongly suggested that you secure this file to prevent other users gaining access to your database. To do this you should type the following:

```
chown <myuser> my.ini
chmod 0600 my.ini
```

substituting '<myuser>' for the username of the account that will be running the script.

## The py_linkcheck.py script
There is one operational setting that can be made within the script. This setting declares the maximum number of active web calls, or agents, that the script should use at any one time.

The variable is named 'workers' and is declared on line 83. This is an integer variable and the value sets the number of concurrent web agents the script should use. The higher this value is the more number of web agents the script will use. There are however limitations on the amount of web agents that the script can support. The number of web agents that the script can run concurrently is limited by factors such as network bandwidth, system memory and overall system load.

The 'workers' variable is also used when setting up the connection pool to the mysql database. By default a mysql database will support upto a maximum of 32 concurrent connections. You will need to contact your DBA to find out what limits may be applied to your database.

Once you have the script setup and configured running the script is as easy as:

'python py_linkcheck.py'
