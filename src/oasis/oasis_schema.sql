-- Created by Vertabelo (http://vertabelo.com)


-- tables
-- Table: applications
DROP TABLE IF EXISTS applications;
/* CREATE TABLE applications (
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
); */ -- Applications was intended to allow someone to apply to be a host or admin

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


-- Table: places represents the physical location 
DROP TABLE IF EXISTS places;
CREATE TABLE places (
    id integer NOT NULL CONSTRAINT places_pk PRIMARY KEY,
    place_name varchar(100) NOT NULL,
    owner_id integer NOT NULL,
    loc_lon double NOT NULL, -- location longitude
    loc_lat double NOT NULL, -- location latitude
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
    type_id integer NOT NULL, -- 1 represents a role of Admin, 2 represents a role of Host, 3 represents a role of Artist, 4 represents a role of Visitor (someone logged in but none of the above roles)
    item integer NOT NULL,
    CONSTRAINT users_users_favorites FOREIGN KEY (user_id)
    REFERENCES users (id),
    CONSTRAINT users_favorites_favorites_types FOREIGN KEY (type_id)
    REFERENCES favorites_types (id)
);

-- Table: events represents an artwork being hosted at a specific location during a particular time period
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
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('1', 'Admin', 'Admin', 'admin@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '1');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('2', 'Maggie', 'M', 'maggiem@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('3', 'Sian', 'K', 'siank@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('4', 'Aliza', 'R', 'alizar@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('5', 'Peter', 'P', 'peterp@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('6', 'Gina', 'R', 'ginar@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('7', 'Brandon', 'L', 'brandonl@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '2');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('8', 'Rob', 'K', 'robk@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('9', 'Melissa', 'T', 'melissat@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('10', 'Lia', 'L', 'lial@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('11', 'Ronie', 'B', 'ronieb@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('12', 'Brenda', 'M', 'brendam@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('13', 'Jane', 'H', 'janeh@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('14', 'John', 'D', 'johnd@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('15', 'StreetGrit', 'StreetGrit', 'streetgrit@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('16', 'Mary Lynn', 'D', 'marylynnd@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('17', 'Marcus', 'B', 'marcusb@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('18', 'JJK', 'JJK', 'jjk@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('19', 'Tanit', 'F', 'tanitf@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('20', 'Colin', 'S', 'colins@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('21', 'Alina', 'V', 'alinav@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('22', 'Patrick', 'B', 'patrickb@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`, `user_password`, `user_role`) VALUES ('23', 'Lindsey', 'unkown', 'lindsey@oasis.com', '8E424DB8E5664ADE76226356BCF5EF6AD9D0879BDAD6377DB835868B17C443BA', '3');

/* Example DB entries for places */

INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('100', 'CREATE', '3', '42.388228', '-71.099655');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('101', 'Nuclear Bean', '2', '42.360574', '-71.105250');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('102', 'Runners Paradise', '4', '42.341653', '-71.076217');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('103', 'Purple Turtle', '7', '42.380412', '-71.095088');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('104', 'Garden', '2', '42.360087', '-71.065992');
INSERT INTO places (`id`, `place_name`, `owner_id`, `loc_lon`, `loc_lat`) VALUES ('105', 'Wall on Mass', '5', '42.367756', '-71.107348');

/* Example DB entries for events YYYY-MM-DD HH:MI:SS */

INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('500', '100', '8', '', '2019-03-27 00:00:00', '2019-04-27 00:00:00', '');
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('501', '101', '9', '', '2019-02-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('502', '102', '10', '', '2019-04-01 00:00:00', '2019-04-05 00:00:00', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('503', '103', '11', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('504', '104', '11', '', '2019-03-01 00:00:00', '2019-03-10 00:00:00', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('505', '105', '12', '', '2019-03-01 00:00:00', '2019-04-01 18:00:00', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('506', '100', '13', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('507', '100', '14', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('508', '101', '15', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('509', '101', '16', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('510', '102', '17', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('511', '102', '18', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('512', '103', '19', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('513', '103', '20', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('514', '104', '21', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('515', '104', '22', '', '2019-03-01 00:00:00', '', ''); 
INSERT INTO events (`id`, `place_id`, `artist_id`, `description`, `start_date`, `end_date`, `photo`) VALUES ('516', '105', '23', '', '2019-04-01 08:00:00', '', ''); 

-- End of file.

