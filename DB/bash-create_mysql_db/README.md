# create_mysql_db

This script will connect to an existing mysql host to:
* Create a new DB
* Create new user
* Grant the new user full privileges on the newly created db.

### Prerequisites:
* [MySQL Client](https://dev.mysql.com/doc/refman/8.0/en/programs-client.html)

### Usage:
```bash
OPTIONS:
   -h	Show this message
   -H	Database hostname or IP address
   -U	Database Root user name
   -P	Database Root user password
   -u	user to create name
   -p	user to create password
   -d	database to create name

Example:
./createdb.sh -H DBHostname \
-H DBHostname \
-U RootUser \
-P RootUserPass \
-d NewDBName \
-u NewDBUser \
-p NewDBUserPass
```
