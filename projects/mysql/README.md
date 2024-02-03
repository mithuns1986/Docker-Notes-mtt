# Project: Setting Up MySQL Database Using Docker

## Objective

The goal of this project is to set up a MySQL database using Docker. This is a beginner-friendly project designed to introduce Docker containerization concepts and basic database management skills.

## Skills Learned

- Docker container management
- Basic MySQL database administration
- Data persistence in Docker
- Basic SQL queries for database interaction

## Tools Needed

- Docker installed on your system
- Terminal or command prompt access
- Optional: SQL client tool for database interaction (like MySQL Workbench, DBeaver, or phpMyAdmin)

## System Diagram

```
+--------------------------+
|  Local Machine           |
|  (Your Computer)         |
|  +--------------------+  |
|  | Docker             |  |
|  | +-----------+      |  |       +--------------------------------+
|  | | MySQL     |<--------------->| SQL Management Tool            |
|  | | Container |      |  |       | (Accessing & Managing Database)|
|  | +-----------+      |  |       +--------------------------------+
|  |       ^            |  |
|  |       |            |  |
|  |       v            |  |
|  |  +--------------+  |  |
|  |  | Data Volume  |  |  |
|  |  | (For         |  |  |
|  |  | Persistence) |  |  |
|  |  +--------------+  |  |
|  +--------------------+  |
+--------------------------+
```

### Launching the MySQL Container

Initiate a MySQL container instance. It's handy to name your container, which allows you to refer to it easily later:

```
docker run -d --name mysql_container -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret_pass mysql:latest
```

- `--name mysql_container`: Assigns the name "mysql_container" to our container.
- `-p 3306:3306`: Maps port 3306 on the host to port 3306 on the container.
- `-e MYSQL_ROOT_PASSWORD=secret_pass`: Sets the root password for MySQL to "secret_pass".

### Accessing MySQL Inside the Container

Once the container is running, you can execute commands within:

```bash
docker exec -it mysql_container bash
mysql -u root -p
```

You will be prompted for the password. Enter secret_pass, the password you set during container creation.

### Creating a Database

Within the MySQL prompt, you can set up your database and tables:

```MySQL
-- Create a new database named 'sample_db'
CREATE DATABASE sample_db;
-- Display all databases to verify our creation
SHOW DATABASES;
-- Select 'sample_db' for subsequent operations
USE sample_db;
```

### Setting up a Sample Table

Let's create a table named items as an example:

```MySQL
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Now, you have a MySQL container with a sample_db database and an items table. This setup can serve as a starting point for a variety of applications, from web services to data analytics. Adjust the table schemas to fit the specific needs of your projects.
