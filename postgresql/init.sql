CREATE TABLE posts (
  id serial NOT NULL,
  title VARCHAR(30) NOT NULL,
  content VARCHAR(2000) NOT NULL,
  user_id INT,
  publish_status INT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
)
