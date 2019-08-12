#!/bin/bash

# Display the help text
HELPTEXT()
{
    cat << EOF
usage: $0 [-h] -H [DB hostname/ip] -U [DB ROOT user name] -P [DB ROOT user password] -d [DB name] -u [DB user name] -p [DB user password]
    This script will create: a new database, a new user and grant that user full privileges on the created db.
    OPTIONS:
       -h	Show this message
       -H	Database hostname or IP address
       -U	Database Root user name
       -P	Database Root user password
       -u	user to create name
       -p	user to create password
       -d	database to create name

 Example:
  $0 -H DBHostname \\
	 -U RootUser \\
	 -P RootUserPass \\
	 -d NewDBName \\
	 -u NewDBUser \\
	 -p NewDBUserPass
EOF
}


# === Command line args ===
while getopts hH:U:P:u:p:d: arg; do
        case $arg in
                h) HELPTEXT
                   exit -1
                   ;;
                H) HOST=$OPTARG
                   ;;
                U) ROOTUSER=$OPTARG
                   ;;
                P) ROOTPASS=$OPTARG
                   ;;
                u) LOCUSER=$OPTARG
                   ;;
                p) LOCPASS=$OPTARG
                   ;;
                d) DBNAME=$OPTARG
                   ;;
        		?) echo "Option/s error/s"
        		   HELPTEXT
        		   exit -1
        		   ;;
        esac
done

if [ $# -eq 0 ]; then
	echo -e "\033[0;31mInvalid entry arguments\033[0m"
	HELPTEXT
	exit 1
fi

MYSQL=$(which mysql)
Q1="DROP USER IF EXISTS '$LOCUSER';"
Q2="CREATE USER '$LOCUSER'@'%';"
Q3="CREATE DATABASE IF NOT EXISTS $DBNAME;"
Q4="GRANT ALL ON $DBNAME.* TO '$LOCUSER'@'%' IDENTIFIED BY '$LOCPASS';"
Q5="FLUSH PRIVILEGES;"
SQL="${Q1}${Q2}${Q3}${Q4}${Q5}"

echo -e "SQL COMMANDS TO RUN on $HOST:\n${SQL}\n"

read -p "Continue (y/n)?" choice
case "$choice" in
  y|Y ) echo -e "yes - execute script...\n";;
  n|N ) echo -e "no - cancel execution"; exit 0;;
  * ) echo -e "invalid response"; exit -1;;
esac

$MYSQL -h $HOST -u $ROOTUSER -p"${ROOTPASS}" -e "${SQL}"
