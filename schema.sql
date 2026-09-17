-- PostgreSQL production target schema. The included demo API uses SQLite so it can run without a database server.
CREATE TABLE IF NOT EXISTS drivers (
  id VARCHAR(64) PRIMARY KEY,
  name TEXT NOT NULL,
  mobile VARCHAR(20),
  license VARCHAR(64),
  vehicle_reg VARCHAR(64),
  vehicle_model VARCHAR(64),
  dealer TEXT,
  location TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS attempts (
  attempt_id VARCHAR(100) PRIMARY KEY,
  driver_id VARCHAR(64) NOT NULL REFERENCES drivers(id),
  quiz_type VARCHAR(64) NOT NULL,
  date_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  score INTEGER,
  percentage INTEGER,
  total INTEGER,
  question_ids JSONB NOT NULL,
  answers JSONB NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_attempt_driver ON attempts(driver_id);
