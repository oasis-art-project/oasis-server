-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2019-03-05 00:22:24.313

-- tables
-- Table: applications
DROP TABLE IF EXISTS applications;
CREATE TABLE applications (
    id integer NOT NULL CONSTRAINT applications_pk PRIMARY KEY,
    artist_id integer NOT NULL,
    event_id integer NOT NULL,
    host_id integer NOT NULL,
    notes text,
    CONSTRAINT users_artist FOREIGN KEY (artist_id)
    REFERENCES users (id),
    CONSTRAINT events_applications FOREIGN KEY (event_id)
    REFERENCES events (id),
    CONSTRAINT users_host FOREIGN KEY (host_id)
    REFERENCES users (id)
);

-- Table: artworks
DROP TABLE IF EXISTS artworks;
CREATE TABLE artworks (
    id integer NOT NULL CONSTRAINT artworks_pk PRIMARY KEY,
    artist_id integer NOT NULL,
    art_name varchar(200) NOT NULL,
    description text,
    photo text NOT NULL,
    CONSTRAINT artworks_users FOREIGN KEY (artist_id)
    REFERENCES users (id)
);

-- Table: favorites_types
DROP TABLE IF EXISTS favorites_types;
CREATE TABLE favorites_types (
    id integer NOT NULL CONSTRAINT favorites_types_pk PRIMARY KEY,
    type varchar(100) NOT NULL
);

-- Table: messages
DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    id integer NOT NULL CONSTRAINT messages_pk PRIMARY KEY,
    sender_id integer NOT NULL,
    recipient_id integer NOT NULL,
    message text NOT NULL,
    CONSTRAINT users_recipient FOREIGN KEY (recipient_id)
    REFERENCES users (id),
    CONSTRAINT users_sender FOREIGN KEY (sender_id)
    REFERENCES users (id)
);

-- Table: places
DROP TABLE IF EXISTS places;
CREATE TABLE places (
    id integer NOT NULL CONSTRAINT places_pk PRIMARY KEY,
    place_name varchar(100) NOT NULL,
    owner_id integer NOT NULL,
    loc_lon double NOT NULL,
    loc_lat double NOT NULL,
    CONSTRAINT places_users FOREIGN KEY (owner_id)
    REFERENCES users (id)
);

-- Table: users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id integer NOT NULL CONSTRAINT users_pk PRIMARY KEY,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(64) NOT NULL,
    user_role tinyint NOT NULL
);

-- Table: users_favorites
DROP TABLE IF EXISTS users_favorites;
CREATE TABLE users_favorites (
    id integer NOT NULL CONSTRAINT users_favorites_pk PRIMARY KEY,
    user_id integer NOT NULL,
    type_id integer NOT NULL,
    item integer NOT NULL,
    CONSTRAINT users_users_favorites FOREIGN KEY (user_id)
    REFERENCES users (id),
    CONSTRAINT users_favorites_favorites_types FOREIGN KEY (type_id)
    REFERENCES favorites_types (id)
);

-- Table: events
DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id integer NOT NULL CONSTRAINT events_pk PRIMARY KEY,
    place_id integer NOT NULL,
    event_name varchar(500) NOT NULL,
    description text,
    start_date datetime NOT NULL,
    end_date datetime,
    photo text,
    CONSTRAINT events_places FOREIGN KEY (place_id)
    REFERENCES places (id)
);

INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('1', 'Admin', 'Admin', 'admin@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '1');

-- End of file.

