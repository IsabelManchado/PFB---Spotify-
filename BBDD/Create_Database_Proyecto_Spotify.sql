CREATE DATABASE Proyecto_Spotify;

USE Proyecto_Spotify;

CREATE TABLE artistas (
    artista_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE canciones (
    cancion_id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    artista_id INT,
    duracion_segundos FLOAT NOT NULL,
    popularidad INT DEFAULT 0,
    explicito BOOLEAN DEFAULT FALSE,
    fecha_lanzamiento DATE,
    danceability FLOAT CHECK (danceability BETWEEN 0 AND 1),
    energy FLOAT CHECK (energy BETWEEN 0 AND 1),
    valence FLOAT CHECK (valence BETWEEN 0 AND 1),
    tempo FLOAT,
    acousticness FLOAT CHECK (acousticness BETWEEN 0 AND 1),
    instrumentalness FLOAT CHECK (instrumentalness BETWEEN 0 AND 1),
    speechiness FLOAT CHECK (speechiness BETWEEN 0 AND 1),
    url_spotify VARCHAR(255),
    imagen TEXT,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artista_id) REFERENCES artistas(artista_id)
		ON DELETE SET NULL
        ON UPDATE CASCADE
);