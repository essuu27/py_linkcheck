# py_linkcheck
Check the validity and availability of a large list of URLs

## Introduction
This script is designed to check whether the entries in a long list of URLs are still valid and available. The script uses a mysql database 
to hold the list of URLs and also as a transaction-state table so that the script is aware of what URLs have been already checked and which 
are currently being analysed.

## Setup
To use this script you will first have to setup a mysql database table to hold the list of URLs that are to be analysed. The table should have 
the following format:

| ID      | URL | Result      | Datetime |

- The 'ID' column should be setup as the 'primary key' and also set to auto-increment.
- The 'Datetime' column should have an attribute set as "ON UPDATE CURRENT_TIMESTAMP". This is **NOT** mandatory as it is meant to give the 
script operator an indication of the date and time that a particular URL has been checked.

If it is required/wanted that the timestamp feature is available but the user cannot set this attribute on their database then the script's code 
has a commented out section that will update the column as required.

Once the database has been created then it can be populated with a list of URLs. Importing a CSV file where each line hold a URL preceded by a 
comma ',' should be all that is needed to setup your database.
