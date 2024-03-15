SELECT movies.title, ratings.rating
FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE movies.year = 2010
ORDER BY ratings.rating DESC, movies.title ASC;
