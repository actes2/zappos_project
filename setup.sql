CREATE DATABASE zappos;

USE zappos;

CREATE TABLE accounts (
    `key` INT AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(100),
    PRIMARY KEY (`key`)
);

CREATE TABLE details (
    `key` INT AUTO_INCREMENT,
    location VARCHAR(100),
    company VARCHAR(100),
    dogs INT,
    PRIMARY KEY (`key`)
);

CREATE TABLE extra (
    `key` INT AUTO_INCREMENT,
    house_number INT,
    windows INT,
    doors INT,
    garages INT,
    floors INT,
    town VARCHAR(100),
    age INT,
    PRIMARY KEY (`key`)
);