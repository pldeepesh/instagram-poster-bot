CREATE TABLE apod_responses (
    id SERIAL PRIMARY KEY,
    date DATE,
    title varchar(1000),
    explanation TEXT,
    URL varchar(1000),
    media_type varchar(500),
    copyright TEXT,
    service_version varchar(100),
    hdurl TEXT,
    api_full_response JSONB NOT NULL,
    api_start_ts TIMESTAMP,
    api_end_ts TIMESTAMP,
    api_status_code integer,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tags TEXT
);

CREATE TABLE insta_posts (
    id SERIAL PRIMARY KEY,
    apod_responses_id INT,
    final_url varchar(1000),
    caption text,
    tags text,
    posted_to_instagram BOOLEAN DEFAULT false,
    insta_post_time TIMESTAMP,
    reason varchar(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_apod_responses
    FOREIGN KEY(apod_responses_id)
    REFERENCES apod_responses(id)
);


GRANT ALL ON DATABASE starry_post_daily TO insta_bot;

GRANT ALL ON apod_responses TO insta_bot ;
GRANT USAGE, SELECT ON SEQUENCE apod_responses_id_seq TO insta_bot;

GRANT ALL ON insta_posts TO insta_bot ;
GRANT USAGE, SELECT ON SEQUENCE insta_posts_id_seq TO insta_bot;
