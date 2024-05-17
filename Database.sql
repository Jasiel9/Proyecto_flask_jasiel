CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    contrasena VARCHAR(255)
);

CREATE TABLE Gastos (
    id_gasto INT PRIMARY KEY AUTO_INCREMENT,
    tipo_transaccion ENUM('Alimentacion', 'Transportacion', 'Entretenimiento'),
    descripcion VARCHAR(255),
    precio DOUBLE,
    fecha DATE
);

ALTER TABLE Gastos
ADD id_gasto INT AUTO_INCREMENT PRIMARY KEY FIRST;


-- Insertar algunos datos de prueba
INSERT INTO Usuarios (nombre, apellido, email, contrasena) VALUES
('John', 'Doe', 'john.doe@example.com', 'password1'),
('Jane', 'Smith', 'jane.smith@example.com', 'password2'),
('Alice', 'Johnson', 'alice.johnson@example.com', 'password3');

-- Insertar transacciones de Alimentación
INSERT INTO Gastos (tipo_transaccion, descripcion, precio, fecha) VALUES
    ( 'Alimentacion', 'Subway', 10.50, '2024-05-05'),
    ( 'Alimentacion', 'Pizza Hut', 25.75, '2024-05-12'),
    ( 'Alimentacion', 'Burger King', 18.20, '2024-05-18');

-- Insertar transacciones de Transportación
INSERT INTO Gastos (tipo_transaccion, descripcion, precio, fecha) VALUES
    ( 'Transportacion', 'Uber', 30.00, '2024-05-07'),
    ( 'Transportacion', 'Taxi', 15.50, '2024-05-14');

-- Insertar transacciones de Entretenimiento
INSERT INTO Gastos ( tipo_transaccion, descripcion, precio, fecha) VALUES
    ( 'Entretenimiento', 'Cine', 20.00, '2024-05-10'),
    ( 'Entretenimiento', 'Parque de diversiones', 35.50, '2024-05-22');



  
 