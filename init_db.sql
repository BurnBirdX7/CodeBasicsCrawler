
CREATE SCHEMA courses;

CREATE TABLE courses."source" (
	id serial NOT NULL,
	url varchar NULL,
    CONSTRAINT courses_pk PRIMARY KEY (id)
);


CREATE TABLE courses."level" (
	id serial NOT NULL,
	"text" varchar NULL,
	CONSTRAINT level_pk PRIMARY KEY (id)
);


CREATE TABLE courses.course_metadata (
	id serial4 NOT NULL,
	source_id int4 NULL,
	url varchar NULL,
	last_update timestamp NULL,
	date_start timestamp NULL,
	date_end timestamp NULL,
	level_id int4 NULL,
	price varchar NULL,
	price_other varchar NULL,
	author varchar NULL,
	price_currency varchar NULL,
	duration interval NULL,
	CONSTRAINT course_metadata_pk PRIMARY KEY (id),
	CONSTRAINT course_metadata_source_fk FOREIGN KEY (source_id) REFERENCES courses."source"(id) ON DELETE CASCADE ,
	CONSTRAINT course_metadata_level_fk FOREIGN KEY (level_id) REFERENCES courses."level"(id) ON DELETE CASCADE
);


CREATE TABLE courses.course_raw (
	course_id int4 NOT NULL,
	title varchar NULL,
	section_title varchar NULL,
	preview varchar NULL,
	description varchar NULL,
	"program" varchar NULL,
	course_keys varchar NULL,
	CONSTRAINT course_raw_pk PRIMARY KEY (course_id),
	CONSTRAINT course_raw_metadata_fk FOREIGN KEY (course_id) REFERENCES courses.course_metadata(id) ON DELETE CASCADE
);


CREATE TABLE courses.reviews (
	id serial4 NOT NULL,
	course_id int4 NULL,
	"text" varchar NULL,
	author varchar NULL,
	"date" timestamp NULL,
	CONSTRAINT reviews_pk PRIMARY KEY (id),
	CONSTRAINT reviews_metadata_fk FOREIGN KEY (course_id) REFERENCES courses.course_metadata(id) ON DELETE CASCADE
);
