-- Origen
-- SELECT * FROM proyecto_spotify.artistas AS A

-- Joins
-- SELECT * FROM proyecto_spotify.canciones AS C

SELECT
A.nombre AS Artista,
C.nombre AS Cancion,
C.duracion_segundos,
C.popularidad,
C.explicito,
C.fecha_lanzamiento,
C.danceability,
C.energy,
C.valence,
C.tempo,
C.acousticness,
C.instrumentalness,
C.speechiness

FROM proyecto_spotify.artistas AS A

-- Joins
LEFT JOIN proyecto_spotify.canciones AS C ON A.artista_id = C.artista_id

-- Condicionales
WHERE C.popularidad > 80
AND C.explicito = '1'
ORDER BY C.popularidad DESC