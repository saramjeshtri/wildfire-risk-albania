CREATE TABLE fires (
    id SERIAL PRIMARY KEY,
    latitude NUMERIC,
    longitude NUMERIC,
    bright_ti4 NUMERIC,
    bright_ti5 NUMERIC,
    scan NUMERIC,
    track NUMERIC,
    frp NUMERIC,
    acq_date DATE,
    acq_time TEXT,
    satellite TEXT,
    instrument TEXT,
    confidence TEXT,
    version TEXT,
    daynight TEXT,
    source TEXT
);