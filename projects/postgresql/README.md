## Setting Up a PostgreSQL Docker Container

In this guide, we'll demonstrate how to deploy a PostgreSQL container using Docker and establish a sample database with tables to help you start.

### Launching the PostgreSQL Container

Start by initiating a PostgreSQL container instance. Naming your container is beneficial as it enables easy referencing later:

```bash
docker run -d --name postgres_container -p 5432:5432 -e POSTGRES_PASSWORD=secret_pass postgres:latest
```

- `--name postgres_container`: Assigns the name "postgres_container" to our container.
- `-p 5432:5432`: Maps port 5432 on the host to port 5432 on the container.
- `-e POSTGRES_PASSWORD=secret_pass`: Sets the password for the default PostgreSQL user "postgres" to "secret_pass".

### Accessing PostgreSQL Inside the Container

Once the container is running, access the PostgreSQL prompt as follows:

```bash
docker exec -it postgres_container psql -U postgres
```

You'll be automatically connected to PostgreSQL. When prompted for a password, enter secret_pass, the password you set during container creation.

### Creating a Database

Within the PostgreSQL prompt, set up your database and tables:

```SQL
-- Create a new database named 'sample_db'
CREATE DATABASE sample_db;
-- Connect to 'sample_db' for subsequent operations
\c sample_db;
```

### Setting up a Sample Table

Let's create a products table as an example:

```SQL
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    date_added TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Now, you have a PostgreSQL container running with a sample_db database and a products table. This basic setup can be the foundation for various applications, from web platforms to data analysis tools. Modify the table structures to match the specific requirements of your projects.
