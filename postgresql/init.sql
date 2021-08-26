CREATE TABLE IF NOT EXISTS posts (
  id serial NOT NULL,
  title VARCHAR(30) NOT NULL,
  content VARCHAR(2000) NOT NULL,
  user_id INT,
  publish_status INT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
  id serial NOT NULL,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  profile VARCHAR(400) NOT NULL,
  encrypted_password VARCHAR(50) NOT NULL,
  authority_classification INT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS relations (
  id serial NOT NULL,
  follow_id INT REFERENCES users(id),
  follower_id INT REFERENCES users(id),
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS likes (
  id serial NOT NULL,
  user_id INT REFERENCES users(id),
  post_id INT REFERENCES posts(id),
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX ON likes (user_id, post_id);

CREATE TABLE IF NOT EXISTS comments (
  id serial NOT NULL,
  content VARCHAR(400) NOT NULL,
  user_id INT REFERENCES users(id),
  post_id INT NOT NULL REFERENCES posts(id),
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX ON comments (post_id);

CREATE TABLE IF NOT EXISTS categories (
  id serial NOT NULL,
  name VARCHAR(400) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX ON categories (name);

CREATE TABLE IF NOT EXISTS post_categories (
  id serial NOT NULL,
  post_id INT REFERENCES posts(id),
  category_id INT REFERENCES categories(id),
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX ON post_categories (post_id);
CREATE INDEX ON post_categories (category_id);
