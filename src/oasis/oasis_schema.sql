-- Created by Vertabelo (http://vertabelo.com)


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
    user_password varchar(64) NOT NULL,
    user_role tinyint NOT NULL, /* an integer of 1 represents Admin, 2 is 								Host, 3 is Artist, 4 is Visitor */
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
    artist_id integer NOT NULL,
    description text,
    start_date datetime NOT NULL,
    end_date datetime,
    photo text,
    FOREIGN KEY place_id REFERENCES places(id)
    FOREIGN KEY artist_id REFERENCES users(id)
);

/* Exaple DB entries for users */
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('1', 'Admin', 'Admin', 'admin@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '1');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('2', 'Maggie', 'M', 'maggiem@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('3', 'Sian', 'K', 'siank@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('4', 'Aliza', 'R', 'alizar@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('5', 'Peter', 'P', 'peterp@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('6', 'Gina', 'R', 'ginar@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('7', 'Brandon', 'L', 'brandonl@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('8', 'Rob', 'K', 'robk@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('9', 'Melissa', 'T', 'melissat@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('10', 'Lia', 'L', 'lial@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('11', 'Ronie', 'B', 'ronieb@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('12', 'Brenda', 'M', 'brendam@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('13', 'Jane', 'H', 'janeh@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('14', 'John', 'D', 'johnd@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('15', 'StreetGrit', 'StreetGrit', 'streetgrit@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('16', 'Mary Lynn', 'D', 'marylynnd@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('17', 'Marcus', 'B', 'marcusb@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('18', 'JJK', 'JJK', 'jjk@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('19', 'Tanit', 'F', 'tanitf@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('20', 'Colin', 'S', 'colins@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('21', 'Alina', 'V', 'alinav@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('22', 'Patrick', 'B', 'patrickb@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `email`, `password`, `user_role`) VALUES ('23', 'Lindsey', 'unkown', 'lindsey@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');

/* Example DB entries for places */

INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('100', 'CREATE', '3', '42.388228', '-71.099655');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('101', 'Nuclear Bean', '2', '42.360574', '-71.105250');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('102', 'Runners Paradise', '4', '42.341653', '-71.076217');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('103', 'Purple Turtle', '7', '42.380412', '-71.095088');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('104', 'Garden', '2', '42.360087', '-71.065992');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('105', 'Wall on Mass', '5', '42.367756', '-71.107348');

/* Example DB entries for events */

-- End of file.

