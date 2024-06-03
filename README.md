# CMSC 127 S-4L AY 2023-2024 PROJECT 
- Project GitHub Repository: https://github.com/jabaleda/cmsc127-lab-proj

# MEMBERS:
- Julianne Paulene Baleda
- Kaye Chantal Pabico
- Jem De Venecia

# How to Setup the Database?
1. Open the terminal and go to the directory of the project folder
2. login to your sql root 
    mysql -uroot -p
3. run the sql dump file
    source database_mysql.sql;
4. Exit to your root
    exit;
5. Log in as 'cmsc127'
    mysql -ucmsc127 -pproject
6. Use the 'cmsc127project' database
    use cmsc127project;

# How to Run the application?
1. In the mdb_connector.py file, change the username and password according to the credentials of your root in sql
2. Once you change it, run the application through the file main.py

# References
- Python Syntax - https://www.w3schools.com/python/python_syntax.asp
- Python 3.12.3 documentation - https://docs.python.org/3.12/index.html
- How To Store and Retrieve Data in MariaDB Using Python on Ubuntu 18.04 - https://www.digitalocean.com/community/tutorials/how-to-store-and-retrieve-data-in-mariadb-using-python-on-ubuntu-18-04 
- Python MySQL Database Connection using MySQL Connector - https://pynative.com/python-mysql-database-connection/
- Python Insert Into MySQL Table - https://pynative.com/python-mysql-insert-data-into-database-table/
- MariaDB Documentation - https://mariadb.com/kb/en/documentation/
