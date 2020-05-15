// SELECT users.first_name, COUNT(posts.id) AS post_count
// FROM users
// LEFT JOIN posts
// ON posts.user_id = users.id
// WHERE posts.user_id = users.id
// GROUP BY users.first_name
// ORDER BY COUNT(posts.id);