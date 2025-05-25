DROP TABLE IF EXISTS scan;
DROP TABLE IF EXISTS badge;
DROP TABLE IF EXISTS display;
DROP TABLE IF EXISTS media;
PRAGMA foreign_keys = ON;

CREATE TABLE media
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    url        VARCHAR(255) NOT NULL,
    sample     BOOLEAN      NOT NULL DEFAULT FALSE,
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
    p1_media_id INTEGER     REFERENCES media (id) ON DELETE SET NULL,
    p1_score    INT         NOT NULL DEFAULT 0,
    -- player 2
    p2_name     VARCHAR(10) NOT NULL,
    p2_media_id INTEGER     REFERENCES media (id) ON DELETE SET NULL,
    p2_score    INT         NOT NULL DEFAULT 0,
    -- identifiers
    code        VARCHAR(36) NOT NULL UNIQUE,
    -- timestamps
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE badge
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    code       VARCHAR(36) NOT NULL UNIQUE,
    name       VARCHAR(50) NOT NULL,
    media_id   INTEGER     REFERENCES media (id) ON DELETE SET NULL,
    -- timestamps
    created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE scan
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    badge_id   INTEGER REFERENCES badge (id) ON DELETE RESTRICT,
    p1_or_p2   BOOLEAN   NOT NULL, -- true for player 1, false for player 2
    -- timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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

CREATE TRIGGER touch_badge_updated_at
    AFTER UPDATE
    ON badge
    FOR EACH ROW
    WHEN (OLD.updated_at < CURRENT_TIMESTAMP) --- this avoid infinite loop
BEGIN
    UPDATE badge SET updated_at=CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER touch_scan_updated_at
    AFTER UPDATE
    ON scan
    FOR EACH ROW
    WHEN (OLD.updated_at < CURRENT_TIMESTAMP) --- this avoid infinite loop
BEGIN
    UPDATE scan SET updated_at=CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- seed some sample data
INSERT INTO media (id, url, sample)
VALUES (1, 'default_1.jpg', TRUE),
       (2, 'default_2.jpg', TRUE),
       (3, 'default_3.jpg', TRUE);

INSERT INTO badge (id, code, name, media_id)
VALUES (1, 'default_1', 'Skaev', 1),
       (2, 'default_2', 'Klyx', 2),
       (3, 'default_3', 'TyLo', 3);