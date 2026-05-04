CREATE TABLE IF NOT EXISTS Users
(pwd VARCHAR(50) NOT NULL CHECK(LENGTH(pwd) >= 5),
 username VARCHAR(50) NOT NULL UNIQUE CHECK (LENGTH(username) >= 3),
 email VARCHAR(100) NOT NULL UNIQUE,
 U_id INT,
 PRIMARY KEY(U_id));

CREATE TABLE IF NOT EXISTS Collection
(c_id INT,
 U_id INT NOT NULL,
 PRIMARY KEY(c_id),
 FOREIGN KEY(U_id)
   REFERENCES Users);

CREATE TABLE IF NOT EXISTS MusicGroup
(g_id INT,
 g_name VARCHAR(100) NOT NULL UNIQUE,
 members INT NOT NULL CHECK(members > 0),
 PRIMARY KEY(g_id));

 CREATE TABLE IF NOT EXISTS Musician
(m_id INT,
 m_name VARCHAR(100) NOT NULL,
 PRIMARY KEY(m_id));

 CREATE TABLE IF NOT EXISTS Releases
(title VARCHAR(100) NOT NULL,
 contributors VARCHAR(100) NOT NULL,
 r_type VARCHAR(25) NOT NULL CHECK(r_type IN ('Album', 'EP', 'Single', 'Compilation')),
 format VARCHAR(25) NOT NULL CHECK(format IN ('Digital', 'CD', 'Vinyl', 'Cassette')),
 r_date DATE NOT NULL CHECK(r_date <= CURRENT_DATE),
 r_label VARCHAR(100) NOT NULL,
 cover VARCHAR(275),
 details VARCHAR(200),
 PRIMARY KEY(title, contributors));

 CREATE TABLE IF NOT EXISTS Track
(title VARCHAR(100) NOT NULL,
 r_title VARCHAR(100) NOT NULL,
 r_contributors VARCHAR(100) NOT NULL,
 t_num INT NOT NULL CHECK(t_num > 0),
 duration INT NOT NULL CHECK(duration > 0),
 genre VARCHAR(75) NOT NULL,
 features VARCHAR(100),
 PRIMARY KEY(title, r_title, r_contributors),
 FOREIGN KEY(r_title, r_contributors)
   REFERENCES Releases(title, contributors)
   ON DELETE CASCADE
   ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS Creates
(g_id INT NOT NULL,
 title VARCHAR(100) NOT NULL,
 contributors VARCHAR(100) NOT NULL,
 PRIMARY KEY (g_id, title, contributors),
 FOREIGN KEY(g_id)
   REFERENCES MusicGroup,
 FOREIGN KEY (title, contributors)
   REFERENCES Releases
   ON UPDATE CASCADE
   ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Has
(g_id INT NOT NULL,
 c_id INT NOT NULL,
 m_id INT NOT NULL,
 PRIMARY KEY (c_id, g_id, m_id),
 FOREIGN KEY (g_id)
   REFERENCES MusicGroup,
 FOREIGN KEY (c_id)
   REFERENCES Collection,
 FOREIGN KEY (m_id)
   REFERENCES Musician);


/*
-- Importing CSV Files
-- 1. Users (10 rows)
COPY Users(pwd, username, email, U_id)
FROM '/docker-entrypoint-initdb.d/users.csv'
DELIMITER ','
CSV HEADER;

-- 2. Collection (10 rows)
COPY Collection(c_id, U_id)
FROM '/docker-entrypoint-initdb.d/collection.csv'
DELIMITER ','
CSV HEADER;

-- 3. MusicGroup (10 rows)
COPY MusicGroup(g_id, g_name, members)
FROM '/docker-entrypoint-initdb.d/musicgroup.csv'
DELIMITER ','
CSV HEADER;

-- 4. Musician (17 rows)
COPY Musician(m_id, m_name)
FROM '/docker-entrypoint-initdb.d/musician.csv'
DELIMITER ','
CSV HEADER;

-- 5. Releases (15 rows)
COPY Releases(title, contributors, r_type, format, r_date, r_label, cover, details)
FROM '/docker-entrypoint-initdb.d/releases.csv'
DELIMITER ','
CSV HEADER;

-- 6. Track (45 rows)
COPY Track(title, r_title, r_contributors, t_num, duration, genre, features)
FROM '/docker-entrypoint-initdb.d/track.csv'
DELIMITER ','
CSV HEADER;

-- 7. Creates (15 rows)
COPY Creates(g_id, title, contributors)
FROM '/docker-entrypoint-initdb.d/creates.csv'
DELIMITER ','
CSV HEADER;

-- 8. Has (20 rows)
COPY Has(g_id, c_id, m_id)
FROM '/docker-entrypoint-initdb.d/has.csv'
DELIMITER ','
CSV HEADER;
*/