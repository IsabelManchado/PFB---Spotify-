CREATE DATABASE Proyecto_Spotify;

USE Proyecto_Spotify;

CREATE TABLE artistas (
    artista_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE canciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    artista_id INT REFERENCES artistas(artista_id),
    duracion_segundos FLOAT,
    popularidad INT,
    explicito BOOLEAN,
    fecha_lanzamiento DATE,
    danceability FLOAT,
    energy FLOAT,
    valence FLOAT,
    tempo FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    speechiness FLOAT,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);