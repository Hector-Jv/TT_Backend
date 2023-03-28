USE DB_TT;

INSERT INTO DELEGACION (cveDelegacion, nombreDelegacion) VALUES 
('AOB', 'Álvaro Obregón'),
('AZC', 'Azcapotzalco'),
('BJU', 'Benito Juárez'),
('COY', 'Coyoacán'),
('CUAM', 'Cuajimalpa de Morelos'),
('CUA', 'Cuauhtémoc'),
('GAM', 'Gustavo A. Madero'),
('IZC', 'Iztacalco'),
('IZP', 'Iztapalapa'),
('LMC', 'La Magdalena Contreras'),
('MGH', 'Miguel Hidalgo'),
('MLA', 'Milpa Alta'),
('TLH', 'Tláhuac'),
('TLP', 'Tlalpan'),
('VCA', 'Venustiano Carranza'),
('XOC', 'Xochimilco');

INSERT INTO TIPOSITIO (tipoSitio) VALUES
('Hotel'),
('Restaurante'),
('Museo'),
('Teatro'),
('Parque'),
('Auditorio');

INSERT INTO TIPOUSUARIO (tipoUsuario) VALUES
('Usuario registrado'),
('Administrador');

INSERT INTO SERVICIO (nombreServicio) VALUES
('Gimnasio'),
('Estacionamiento'),
('SPA'),
('Restaurante'),
('Acepta mascotas'),
('Servicio a la habitación'),
('Recepción 24 horas'),
('Translados'),
('Adaptado para personas con movilidad reducida'),
('WIFI'),
('Estación de recarga de vehículos eléctricos'),
('Aire acondicionado');

INSERT INTO ETIQUETA (nombreEtiqueta) VALUES
('Comida rápida'),
('Gourmet'),
('Vegetariana'),
('Casera'),
('Saludable'),
('Mariscos'),
('Picante'),
('Parrilla'),
('Italiana'),
('Mexicana'),
('Japonesa'),
('China'),
('Tailandesa'),
('Naturaleza'),
('Diversión'),
('Aire fresco'),
('Hacer deporte'),
('Tecnología'),
('Historia'),
('Geografía'),
('Economía'),
('Medicina'),
('Animales'),
('Pasar el rato'),
('Lujoso'),
('Barato'),
('Juegos'),
('Pintura'),
('Drama'),
('Suspenso'),
('Comedia'),
('Seguro'),
('Tranquilo'),
('Poca gente'),
('Antojos'),
('Naturaleza'),
('Romantico');

INSERT INTO USUARIO (correo, usuario, contrasena, TIPOUSUARIO_cveTipoUsuario) VALUES
('hectorjv97@gmail.com', 'Israel Jv', '12345', 2),
('manuel@gmail.com', 'Manuel', '12345', 2),
('persona1@gmail.com', 'Persona1', '12345', 1);
