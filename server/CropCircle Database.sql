Create Database CropCircle;
Use CropCircle;

-- 1. User Table
CREATE TABLE User (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    role ENUM('farmer', 'customer', 'admin') NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Farmer Table
CREATE TABLE Farmer (
    farmerId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    farmName VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    farmType VARCHAR(50) NOT NULL,
    certifications TEXT,
    verificationStatus ENUM('pending', 'approved', 'rejected') NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- 3. Product Table
CREATE TABLE Product (
    productId INT AUTO_INCREMENT PRIMARY KEY,
    farmerId INT NOT NULL,
    productName VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    unitPrice DECIMAL(10, 2) NOT NULL,
    stockQuantity INT NOT NULL,
    productImage VARCHAR(255),
    status ENUM('in_stock', 'out_of_stock', 'under_review') DEFAULT 'in_stock',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farmerId) REFERENCES Farmer(farmerId)
);

-- 4. Order Table
CREATE TABLE `Order` (
    orderId INT AUTO_INCREMENT PRIMARY KEY,
    customerId INT NOT NULL,
    orderItems JSON NOT NULL,  -- JSON format for storing an array of productId, quantity, and price
    totalAmount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered') NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customerId) REFERENCES User(userId)
);

-- 5. Cart Table
CREATE TABLE Cart (
    cartId INT AUTO_INCREMENT PRIMARY KEY,
    customerId INT NOT NULL,
    items JSON NOT NULL,  -- JSON format for storing an array of productId and quantity
    totalPrice DECIMAL(10, 2),
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customerId) REFERENCES User(userId)
);


-- 6. Review Table
CREATE TABLE Review (
    reviewId INT AUTO_INCREMENT PRIMARY KEY,
    productId INT NOT NULL,
    customerId INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (productId) REFERENCES Product(productId),
    FOREIGN KEY (customerId) REFERENCES User(userId)
);

-- 7. Admin Activity Log Table
CREATE TABLE AdminActivityLog (
    logId INT AUTO_INCREMENT PRIMARY KEY,
    adminId INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    targetId INT NOT NULL,  -- ID of the target entity (e.g., farmerId or productId)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adminId) REFERENCES User(userId)
);