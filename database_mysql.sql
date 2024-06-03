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
("chanp", "Chan", "chanp@gmail.com", "passw0rd"),
('john_doe', 'John Doe', 'john@example.com', 'password_1'),
('jane_smith', 'Jane Smith', 'jane@example.com', 'password_2'),
('bob_jones', 'Bob Jones', 'bob@example.com', 'password_3');

--insert in foodestablishment

INSERT INTO foodestablishment (name, location) VALUES
('Jollibee', 'Lopez Avenue'),
('Chowking', 'Vega'),
('Cynthia', 'Umali'),
('Mr.Grill', 'Laguna');

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
('Pizza Margherita', 199.00, 'Classic pizza', 4),
('Cheeseburger', 50.00, 'Burger with cheese', 1),
('Sushi Roll', 70.00, 'Fresh salmon', 4),
('Caesar Salad', 110.00, 'With Caesar dressing', 2),
('Spaghetti Carbonara', 80.00, 'Pasta with creamy sauce', 1),
('Tacos', 60.00, 'Corn tortillas with beef', 3),
('Ice Cream Sundae', 20.00, 'Vanilla ice cream', 1),
('French Fries', 40.00, 'Crispy golden fries', 1),
('Chicken Wings', 100.00, 'Spicy fried chicken wings', 4);

-- insert in fooditemtype table
INSERT INTO fooditemtype (itemId, name, foodtypeId, foodType) VALUES
(1, 'Pizza Margherita', 1, 'Meat'),    
(1, 'Pizza Margherita', 2, 'Vegetable'),  
(2, 'Cheeseburger', 1, 'Meat'),        
(3, 'Sushi Roll', 3, 'Seafood'),       
(4, 'Caesar Salad', 2, 'Vegetable'),   
(5, 'Spaghetti Carbonara', 6, 'Pasta'),    
(6, 'Tacos', 1, 'Meat'),               
(7, 'Ice Cream Sundae', 5, 'Dessert'),   
(8, 'French Fries', 6, 'Snack'),       
(9, 'Chicken Wings', 1, 'Meat');       

-- Food reviews
INSERT INTO review (rating, comment, username, itemId) VALUES
(4.5, 'Great pizza!', 'john_doe', 1),  
(4.0, 'Delicious cheeseburger!', 'jane_smith', 2),  
(4.2, 'Amazing sushi!', 'bob_jones', 3),  
(4.3, 'Fresh salad!', 'john_doe', 4),  
(4.6, 'Perfect pasta!', 'jane_smith', 5),  
(4.4, 'Tasty tacos!', 'bob_jones', 6),  
(4.8, 'Yummy ice cream!', 'john_doe', 7),  
(4.7, 'Crunchy fries!', 'jane_smith', 8),  
(4.9, 'Spicy wings!', 'bob_jones', 9);  

-- Establishment reviews
INSERT INTO review (rating, comment, username, establishmentId) VALUES
(4.5, 'Great service!', 'john_doe', 1),  
(4.0, 'Delicious food!', 'jane_smith', 2), 
(4.2, 'Lovely ambiance!', 'bob_jones', 3), 
(4.3, 'Excellent grilled dishes!', 'john_doe', 4);  