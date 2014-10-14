CREATE DATABASE analytics;

CREATE USER 'analytics'@'localhost' IDENTIFIED BY 'analytics';
GRANT ALL PRIVILEGES ON analytics . * TO 'analytics'@'localhost';

FLUSH PRIVILEGES;
