-- Database for Pocket
-- At the moment, sqlite3 only. Probably will stay that way

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER NOT NULL PRIMARY KEY ASC,
    triggers TEXT NOT NULL,
    remark TEXT NOT NULL,
    protected BOOLEAN default false,
    UNIQUE (triggers, remark) ON CONFLICT FAIL
);
