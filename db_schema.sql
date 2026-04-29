-- ============================================
-- VETCARE - SISTEMA DE GESTIÓN VETERINARIA
-- SPRINT 1: ESQUEMA BASE
-- ============================================

DROP DATABASE IF EXISTS vetcare_db;
CREATE DATABASE vetcare_db;
USE vetcare_db;

-- TABLA: DUEÑOS
CREATE TABLE duenos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    direccion VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA: MASCOTAS
CREATE TABLE mascotas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(50),
    edad INT,
    peso DECIMAL(5,2),
    dueno_id INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (dueno_id) REFERENCES duenos(id) ON DELETE CASCADE
);

-- TABLA: HISTORIAL CLÍNICO
CREATE TABLE historial_clinico (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mascota_id INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    diagnostico TEXT NOT NULL,
    tratamiento TEXT,
    observaciones TEXT,
    veterinario VARCHAR(100),
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- TABLA: VETERINARIOS
CREATE TABLE veterinarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA: CITAS
CREATE TABLE citas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mascota_id INT NOT NULL,
    veterinario_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    motivo VARCHAR(200),
    estado ENUM('Agendada', 'Cancelada', 'Completada') DEFAULT 'Agendada',
    creada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id),
    FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id),
    UNIQUE KEY unique_cita (veterinario_id, fecha_hora)
);

-- DATOS INICIALES
INSERT INTO veterinarios (nombre, especialidad, telefono, email) VALUES
('Dr. Juan Pérez', 'Medicina General', '3001234567', 'juan@vetcare.com'),
('Dra. María Gómez', 'Cirugía', '3001234568', 'maria@vetcare.com'),
('Dr. Carlos López', 'Dermatología', '3001234569', 'carlos@vetcare.com');