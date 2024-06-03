DROP DATABASE IF EXISTS cmsc127project;

CREATE OR REPLACE USER 'cmsc127'@'localhost' IDENTIFIED BY 'project';
CREATE DATABASE cmsc127project;
GRANT ALL ON cmsc127project.* TO 'cmsc127'@'localhost';

USE cmsc127project;

CREATE TABLE user (
  username varchar(17) NOT NULL,
  name varchar(25) NOT NULL,
  email varchar(30) NOT NULL,
  password varchar(50) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE adminUser (
  adminId INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(17) NOT NULL,
  email VARCHAR(30) NOT NULL,

  CONSTRAINT adminUser_username_fk FOREIGN KEY (username) REFERENCES user(username)
);

CREATE TABLE foodestablishment (
  establishmentId int(11) NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,
  location varchar(30) NOT NULL,
  PRIMARY KEY (establishmentId)
);

CREATE TABLE foodtype (
  foodtypeId int(11) NOT NULL AUTO_INCREMENT,
  foodType varchar(30) NOT NULL,
  PRIMARY KEY (foodtypeId)
);

CREATE TABLE fooditem (
  itemId int(11) NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,
  price DECIMAL(5, 2) NOT NULL,
  description varchar(30) NOT NULL,
  establishmentId INT NOT NULL,
  PRIMARY KEY (itemId),
  CONSTRAINT fooditem_establishmentId_fk FOREIGN KEY (establishmentId) REFERENCES foodestablishment(establishmentId)
);

CREATE TABLE fooditemtype (
  itemId INT NOT NULL,
  name varchar(30) NOT NULL,
  foodtypeId INT NOT NULL,
  foodType varchar(30) NOT NULL,
  PRIMARY KEY (itemId,foodtypeId),
  CONSTRAINT fooditemtype_foodtypeId_fk FOREIGN KEY (foodtypeId) REFERENCES foodtype (foodtypeId),
  CONSTRAINT fooditemtype_itemId_fk FOREIGN KEY (itemId) REFERENCES fooditem (itemId)
);

CREATE TABLE review (
  reviewId int(11) NOT NULL AUTO_INCREMENT,
  rating decimal(2,1) NOT NULL,
  comment varchar(100) DEFAULT NULL,
  date_reviewed datetime NOT NULL DEFAULT current_timestamp(),
  username varchar(17) NOT NULL,
  establishmentId INT,
  itemId INT,
  PRIMARY KEY (reviewId),
  CONSTRAINT review_establishmentId_fk FOREIGN KEY (establishmentId) REFERENCES foodestablishment (establishmentId),
  CONSTRAINT review_itemId_fk FOREIGN KEY (itemId) REFERENCES fooditem (itemId),
  CONSTRAINT review_username_fk FOREIGN KEY (username) REFERENCES user (username)
);

-- insert in user table
INSERT INTO user VALUES
("tswift", "Taylor Swift", "taylor@example.com", "adminpass"),
('john_doe', 'John Doe', 'john@example.com', 'password_1'),
('jane_smith', 'Jane Smith', 'jane@example.com', 'password_2'),
('bob_jones', 'Bob Jones', 'bob@example.com', 'password_3');

-- insert the admin user into the admin table
INSERT INTO adminUser (username, email)
SELECT username, email
FROM user
WHERE username = 'tswift';

--insert in foodestablishment
INSERT INTO foodestablishment (name, location) VALUES
('Taylor Cafe', 'Nashville'),
('Swift Diner', 'New York'),
('1989 Bakery', 'Los Angeles'),
('Folklore Grill', 'Pennsylvania');

--insert in foodtype
INSERT INTO foodtype (foodType) VALUES
('Meat'),
('Vegetable'),
('Seafood'),
('Fruit'),
('Dessert'),
('Snack');

--insert in fooditem
INSERT INTO fooditem (name, price, description, establishmentId) VALUES
('Red Velvet Cake', 150.00, 'Rich red velvet cake', 3),
('Love Story Latte', 120.00, 'Creamy latte with love', 1),
('Shake It Off Smoothie', 100.00, 'Refreshing fruit smoothie', 4),
('Willow Sandwich', 80.00, 'Delicious turkey sandwich', 2),
('Evermore Espresso', 90.00, 'Strong and bold espresso', 1),
('Fearless Fries', 50.00, 'Crispy golden fries', 3),
('Blank Space Burger', 110.00, 'Juicy cheeseburger', 2),
('Wildest Dreams Pizza', 200.00, 'Pizza with all toppings', 4),
('Delicate Donuts', 60.00, 'Soft and sweet donuts', 1);

-- insert in fooditemtype table
INSERT INTO fooditemtype (itemId, name, foodtypeId, foodType) VALUES
(1, 'Red Velvet Cake', 5, 'Dessert'),    
(2, 'Love Story Latte', 5, 'Dessert'),  
(3, 'Shake It Off Smoothie', 4, 'Fruit'),        
(4, 'Willow Sandwich', 1, 'Meat'),       
(4, 'Willow Sandwich', 2, 'Vegetable'),   
(5, 'Evermore Espresso', 5, 'Dessert'),    
(6, 'Fearless Fries', 6, 'Snack'),               
(7, 'Blank Space Burger', 1, 'Meat'),   
(8, 'Wildest Dreams Pizza', 1, 'Meat'),       
(8, 'Wildest Dreams Pizza', 2, 'Vegetable'),
(9, 'Delicate Donuts', 5, 'Dessert');

-- Food reviews
INSERT INTO review (rating, comment, username, itemId) VALUES
(4.5, 'Amazing cake!', 'john_doe', 1),  
(4.0, 'Delicious latte!', 'jane_smith', 2),  
(4.2, 'Refreshing smoothie!', 'bob_jones', 3),  
(4.3, 'Great sandwich!', 'john_doe', 4),  
(4.6, 'Perfect espresso!', 'jane_smith', 5),  
(4.4, 'Tasty fries!', 'bob_jones', 6),  
(4.8, 'Juicy burger!', 'john_doe', 7),  
(4.7, 'Delicious pizza!', 'jane_smith', 8),  
(4.9, 'Soft and sweet donuts!', 'bob_jones', 9);

-- Establishment reviews
INSERT INTO review (rating, comment, username, establishmentId) VALUES
(4.5, 'Amazing cafe!', 'john_doe', 1),  
(4.0, 'Lovely diner!', 'jane_smith', 2), 
(4.2, 'Great bakery!', 'bob_jones', 3), 
(4.3, 'Excellent grill!', 'john_doe', 4);
