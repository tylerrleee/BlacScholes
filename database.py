import mysql.connector as mariadb



# Create a dictionary (Python's version of a map) to store the configuration info
config = {
    "user": "tienle",  # Change to match your MariaDB Username and Password
    "password": "Thangbom2005", 
    "host": "localhost",
    "database": "quant_app",
    "port": 3306  # Default port for MariaDB
}


# Connect to the MariaDB Server
conn = mariadb.connect(user=config["user"], password=config["password"], host=config["host"], port=config["port"])
cur = conn.cursor()


# Create the database if it doesn't exist, then use it
cur.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']};")
cur.execute(f"USE {config['database']};")


# Create a table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS `inputs` (
  `calc_id`   INT          NOT NULL AUTO_INCREMENT,
  `S`         FLOAT        NOT NULL,
  `K`         FLOAT        NOT NULL,
  `T`         FLOAT        NOT NULL,
  `sigma`     FLOAT        NOT NULL,
  `r`         FLOAT        NOT NULL,
  `C_buy`     FLOAT        NULL,
  `P_buy`     FLOAT        NULL,
  `created_at` TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`calc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")


# Insert a row into the table
cur.execute("""CREATE TABLE IF NOT EXISTS `outputs` (
  `output_id`   INT       NOT NULL AUTO_INCREMENT,
  `calc_id`     INT       NOT NULL,
  `S_shock`     FLOAT     NOT NULL,
  `sigma_shock` FLOAT     NOT NULL,
  `call_val`    FLOAT     NULL,
  `put_val`     FLOAT     NULL,
  `pnl_call`    FLOAT     NULL,
  `pnl_put`     FLOAT     NULL,
  PRIMARY KEY (`output_id`),
  INDEX (`calc_id`),
  CONSTRAINT `fk_outputs_inputs`
    FOREIGN KEY (`calc_id`)
    REFERENCES `inputs` (`calc_id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
            )

# Save the change
conn.commit()


# Read all rows and attributes from the users table
cur.execute("SELECT S, K, T FROM inputs;")


# Get all rows from the table and print them
rows = cur.fetchall()
print(rows)


# Drops the table so this code can be rerun. DO NOT INCLUDE THIS NORMALLY THIS DELETES THE TABLE
cur.execute("drop table inputs;")


# Close the connection
cur.close()
conn.close()