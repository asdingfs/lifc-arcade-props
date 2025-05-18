DROP TABLE IF EXISTS display;
DROP TABLE IF EXISTS media;
PRAGMA foreign_keys = ON;

CREATE TABLE media
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    url        VARCHAR(255) NOT NULL,
    -- timestamps
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE display
(
    -- id database
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    -- player 1
    p1_name     VARCHAR(10) NOT NULL,
    p1_media_id INTEGER     NOT NULL REFERENCES media (id) ON DELETE RESTRICT,
    p1_score    INT         NOT NULL DEFAULT 0,
    -- player 2
    p2_name     VARCHAR(10) NOT NULL,
    p2_media_id INTEGER     NOT NULL REFERENCES media (id) ON DELETE RESTRICT,
    p2_score    INT         NOT NULL DEFAULT 0,
    -- feedback
    code        VARCHAR(36) NOT NULL UNIQUE,
    feedback    TEXT,
    -- timestamps
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER touch_media_updated_at
    AFTER UPDATE
    ON media
    FOR EACH ROW
    WHEN (OLD.updated_at < CURRENT_TIMESTAMP) --- this avoid infinite loop
BEGIN
    UPDATE media SET updated_at=CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER touch_display_updated_at
    AFTER UPDATE
    ON media
    FOR EACH ROW
    WHEN (OLD.updated_at < CURRENT_TIMESTAMP) --- this avoid infinite loop
BEGIN
    UPDATE media SET updated_at=CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE UNIQUE INDEX display_code_key ON display (code);