DROP DATABASE IF EXISTS `news_classifier`;
CREATE DATABASE `news_classifier`;

DROP DATABASE IF EXISTS `news_identifier`;
CREATE DATABASE `news_identifier`;

USE `news_classifier`;
CREATE TABLE dataset(id INT AUTO_INCREMENT, text VARCHAR(1000), category VARCHAR(10), PRIMARY KEY(id));
CREATE INDEX CATEGORY_INDEX ON dataset(category);
CREATE TABLE CLASS_COUNTS_PRIORS(class VARCHAR(20), count INT, prior FLOAT, PRIMARY KEY (class));
CREATE TABLE WORD_CLASS_COUNTS(word VARCHAR(100), class VARCHAR(20), count INT, PRIMARY KEY (word,class));

USE `news_identifier`;
CREATE TABLE dataset(id INT AUTO_INCREMENT, text VARCHAR(1000), category VARCHAR(10), PRIMARY KEY(id));
CREATE INDEX CATEGORY_INDEX ON dataset(category);
CREATE TABLE CLASS_COUNTS_PRIORS(class VARCHAR(20), count INT, prior FLOAT, PRIMARY KEY (class));
CREATE TABLE WORD_CLASS_COUNTS(word VARCHAR(100), class VARCHAR(20), count INT, PRIMARY KEY (word,class));
