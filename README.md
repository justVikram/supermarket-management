## User Guide for Configuring the Application

### Requirements

The following modules must be installed (using pip or conda) in your virtual environment before running the application.

* asgiref==3.3.4
* Django==3.2.3
* mysqlclient==2.0.3
* pytz==2021.1
* sqlparse==0.4.1

## Login Credentials

### Django-Admin Login Credentials

Username: VMART\
Password: vmartadmin

Since Django-admin user is created locally, you will have to create a new superuser after configuring Django using the command: 

```
python manage.py create superuser
```

We recommend using the same credentials as the ones we have used.

### MySQL User Login Credentials

A new user identity will have to be created so that the database can be integrated with Django.Create a new user in MySQL database using the following commands:

```sql
CREATE USER 'VMART'@'localhost' IDENTIFIED BY 'vmartadmin';
GRANT ALL PRIVILEGES ON DBMS_PROJECT.* TO 'VMART'@'localhost' WITH GRANT OPTION;
```