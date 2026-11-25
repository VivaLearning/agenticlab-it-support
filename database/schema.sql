CREATE TABLE IF NOT EXISTS lab_state (
 id integer PRIMARY KEY CHECK(id=1),
 state jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS lab_run (
 id uuid PRIMARY KEY,
 state jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS lab_event (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 run_id uuid REFERENCES lab_run(id),
 event jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now()
);