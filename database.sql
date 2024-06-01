DROP DATABASE IF EXISTS cmsc127project;

CREATE OR REPLACE USER 'cmsc127'@'localhost' IDENTIFIED BY 'project';
CREATE DATABASE cmsc127project;
GRANT ALL ON cmsc127project.* TO 'cmsc127'@'localhost';

USE cmsc127project;

CREATE TABLE foodestablishment (
  establishmentId int(11) NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,
  location varchar(30) NOT NULL,
  PRIMARY KEY (establishmentId)
);

CREATE TABLE fooditem (
  itemId int(11) NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,
  price int(4) NOT NULL,
  description varchar(30) NOT NULL,
  PRIMARY KEY (itemId)
);

CREATE TABLE fooditemtype (
  itemId int(11) NOT NULL,
  name varchar(30) NOT NULL,
  foodtype_id int(11) NOT NULL,
  food_type varchar(30) NOT NULL,
  PRIMARY KEY (itemId,foodtype_id),
  CONSTRAINT fooditemtype_foodtype_id_fk FOREIGN KEY (foodtype_id) REFERENCES foodtype (foodtype_id),
  CONSTRAINT fooditemtype_itemId_fk FOREIGN KEY (itemId) REFERENCES fooditem (itemId)
);

CREATE TABLE foodtype (
  foodtype_id int(11) NOT NULL AUTO_INCREMENT,
  food_type varchar(30) NOT NULL,
  PRIMARY KEY (foodtype_id)
);

CREATE TABLE review (
  reviewId int(11) NOT NULL AUTO_INCREMENT,
  rating decimal(2,1) NOT NULL,
  comment varchar(100) DEFAULT NULL,
  date_reviewed datetime NOT NULL DEFAULT current_timestamp(),
  username varchar(17) NOT NULL,
  establishmentId int(11) NOT NULL,
  itemId int(11) NOT NULL,
  PRIMARY KEY (reviewId),
  CONSTRAINT review_establishmentId_fk FOREIGN KEY (establishmentId) REFERENCES foodestablishment (establishmentId),
  CONSTRAINT review_itemId_fk FOREIGN KEY (itemId) REFERENCES fooditem (itemId),
  CONSTRAINT review_username_fk FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE user (
  username varchar(17) NOT NULL,
  name varchar(25) NOT NULL,
  email varchar(30) NOT NULL,
  password varchar(50) NOT NULL,
  PRIMARY KEY (username)
);
