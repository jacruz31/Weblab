--  Creacion de database
CREATE DATABASE IF NOT EXISTS labremoto;
USE labremoto;

-- Creacion de tablas
CREATE TABLE usuario (
	id varchar(15) NOT NULL, -- Puede ser la cedula o el # de matricula
    nombres varchar(50) NOT NULL,
    apellidos varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
    pass varchar(50) NOT NULL, -- constrasena 
    email varchar(100) NOT NULL,
    cargo varchar(1) default 'e', -- 'e' es para estudiante, 'p' para profesor
    primary key(id)
);

CREATE TABLE laboratorio (
	id int NOT NULL AUTO_INCREMENT,
    materia varchar(50) NOT NULL,
    paralelo int NOT NULL,
    profesor varchar(15),
    primary key(id),
    constraint fk_laboratorio_profesor foreign key (profesor) references usuario(id)
);

CREATE TABLE horario (
	id int NOT NULL AUTO_INCREMENT,
    fecha date NOT NULL,
    hora_inicio time NOT NULL,
    hora_fin time NOT NULL,
    laboratorio int,
    disponible boolean default true,
    primary key(id),
    constraint fk_horario_laboratorio foreign key (laboratorio) references laboratorio(id)
    
);

CREATE TABLE registro (
	id int NOT NULL AUTO_INCREMENT,
    horario int,
    estudiante varchar(15),
    primary key(id),
    constraint fk_registro_estudiante foreign key (estudiante) references usuario(id),
    constraint fk_registro_horario foreign key (horario) references horario(id)
);

-- Datos de ejemplo para insertar
-- Para usuario:
INSERT INTO usuario VALUES ('201805233', 'Carlos Bryan', 'Tomala Reyes', 'ctomala', 'ctomala233', 'cbtomala@espol.edu.ec', 'e');
INSERT INTO usuario VALUES ('201703655', 'Julio Alejandro', 'Cruz Bone', 'jualcruz', 'jacruz655', 'jacruz@espol.edu.ec', 'e');
INSERT INTO usuario VALUES ('200012345', 'Cristopher Javier', 'Vaccaro Cedillo', 'cvaccaro', 'cjvaccaro345', 'cvaccarom@espol.edu.ec', 'p'); -- profesor
INSERT INTO usuario VALUES ('201707205', 'Erick Josue', 'Pulla Zambrano', 'epulla', '12345', 'epulla@espol.edu.ec', 'e');
-- Para laboratorio:
INSERT INTO laboratorio(materia, paralelo, profesor) VALUES ('Laboratorio de Redes de Datos', 101, '200012345');
-- Para horario: (solo hay datos para el primer laboratorio)
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio, disponible) VALUES ('2021-07-30', '08:00:00', '10:00:00', 1, 0);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio) VALUES ('2021-07-25', '10:00:00', '12:00:00', 1);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio) VALUES ('2021-07-31', '12:00:00', '14:00:00', 1);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio) VALUES ('2021-07-26', '14:00:00', '16:00:00', 1);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio, disponible) VALUES ('2021-07-30', '16:00:00', '18:00:00', 1, 0);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio) VALUES ('2021-07-27', '18:00:00', '20:00:00', 1);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio) VALUES ('2021-07-28', '20:00:00', '22:00:00', 1);
INSERT INTO horario(fecha, hora_inicio, hora_fin, laboratorio) VALUES ('2021-07-29', '22:00:00', '00:00:00', 1);
-- Para registro:
INSERT INTO registro(horario, estudiante) VALUES (1, '201707205'); -- Registro para Erick Pulla de 8 a 10 AM
INSERT INTO registro(horario, estudiante) VALUES (5, '201805233'); -- Registro para Carlos Tomala de 4 a 6 PM

-- Para modificar los horarios existentes (por si no se corrigieron las fechas)

update horario set fecha = '2021-07-25' where id = 2;
update horario set fecha = '2021-07-31' where id = 3;
update horario set fecha = '2021-07-26' where id = 4;
update horario set fecha = '2021-07-30' where id = 5;
update horario set fecha = '2021-07-27' where id = 6;
update horario set fecha = '2021-07-28' where id = 8;
update horario set fecha = '2021-07-29' where id = 7;