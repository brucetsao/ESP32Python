CREATE USER 'big'@'localhost' IDENTIFIED VIA mysql_native_password USING '***';GRANT ALL PRIVILEGES ON *.* TO 'big'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;CREATE DATABASE IF NOT EXISTS `big`;GRANT ALL PRIVILEGES ON `big`.* TO 'big'@'localhost';GRANT ALL PRIVILEGES ON `big\_%`.* TO 'big'@'localhost';