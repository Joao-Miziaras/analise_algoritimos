CREATE DATABASE grupo6;
USE grupo6;
CREATE TABLE dados_sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT,
    porcent_umidade FLOAT,
    temperatura FLOAT,
    horario_da_coleta DATETIME
);
select * from dados_sensor;
