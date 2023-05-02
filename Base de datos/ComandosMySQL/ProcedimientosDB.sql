use DB_TT;

show procedure status;

/*Login de usuario registrado y de administrador*/
DELIMITER $$
CREATE PROCEDURE login(IN c_correo VARCHAR(100), IN c_contrasena VARCHAR(100))
BEGIN
	
	CALL validar_usuario(c_correo, c_contrasena);
    DECLARE correo_encontrado INT DEFAULT 0;
    DECLARE contrasena_correcta INT DEFAULT 0;
    
    
    
    -- Buscamos el correo en la tabla USUARIO
    SELECT COUNT(*) INTO correo_encontrado FROM USUARIO WHERE correo = c_correo;
    
    -- Si no encontramos el correo, devolvemos un mensaje de error
    IF correo_encontrado = 0 THEN
        SELECT 'Correo no encontrado' AS mensaje;
    ELSE 
		-- Si encontramos el correo, comparamos las contraseñas
		SELECT COUNT(*) INTO contrasena_correcta FROM USUARIO WHERE correo = c_correo AND contrasena = c_contrasena;
		
        -- Si no coincide la contraseña, devolvemos un mensaje de error
        IF contrasena_correcta = 0 THEN
			SELECT 'Correo o contraseña incorrecto' AS mensaje;
        ELSE
			-- Se dispara un trigger para saber si el usuario es admin o usuario registrado
			SELECT * FROM USUARIO, TIPOUSUARIO WHERE correo = c_correo AND contrasena = c_contrasena AND TIPOUSUARIO_cveTipoUsuario = cveTipoUsuario;
		END IF;
    END IF;
    
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE validar_usuario(IN c_correo VARCHAR(100), IN c_contrasena VARCHAR(100))
BEGIN

    DECLARE correo_encontrado INT DEFAULT 0;
    DECLARE contrasena_correcta INT DEFAULT 0;
    
    -- Buscamos el correo en la tabla USUARIO
    SELECT COUNT(*) INTO correo_encontrado FROM USUARIO WHERE correo = c_correo;
    
    -- No se encontró correo registrado
    IF correo_encontrado = 0 THEN
        SELECT 0;
    ELSE
		-- Se comparan la contraseña con el correo
		SELECT COUNT(*) INTO contrasena_correcta FROM USUARIO WHERE correo = c_correo AND contrasena = c_contrasena;
		
        -- No coincide 
        IF contrasena_correcta = 0 THEN
			SELECT 'Correo o contraseña incorrecto' AS mensaje;
        ELSE
			-- Se dispara un trigger para saber si el usuario es admin o usuario registrado
			SELECT * FROM USUARIO, TIPOUSUARIO WHERE correo = c_correo AND contrasena = c_contrasena AND TIPOUSUARIO_cveTipoUsuario = cveTipoUsuario;
		END IF;
    END IF;
    
END$$
DELIMITER ;



CALL validar_usuario('hectorjv97@gmail.com', '12345');

/*Consulta de preferencias del usuario registrado*/
DELIMITER $$
CREATE PROCEDURE preferencia_usuario (IN c_correo VARCHAR(100))
BEGIN
	SELECT * FROM PREFERENCIA WHERE USUARIO_correo = c_correo;
END$$
DELIMITER ;

/*Consulta de recomendaciones del usuario registrado*/
DELIMITER $$
CREATE PROCEDURE recomendacion_usuario  (IN c_correo VARCHAR(100))
BEGIN
	SELECT * FROM CLUSTERING WHERE USUARIO_correo = c_correo;
END$$
DELIMITER ;



show columns from PREFERENCIA;
CALL preferencia_usuario('hectorjv97@gmail.com');
SHOW PROCEDURE STATUS WHERE Db = 'DB_TT';