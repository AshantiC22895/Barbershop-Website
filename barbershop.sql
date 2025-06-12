CREATE TABLE barbers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

CREATE TABLE services (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    price DECIMAL(5,2)
);

CREATE TABLE availability (
    id INT PRIMARY KEY AUTO_INCREMENT,
    barber_id INT,
    available_date DATE,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (barber_id) REFERENCES barbers(id)
);

CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    service_id INT,
    barber_id INT,
    appointment_time DATETIME,
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (barber_id) REFERENCES barbers(id)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    barber VARCHAR(100),
    service VARCHAR(100),
    appointment_time DATETIME
);

