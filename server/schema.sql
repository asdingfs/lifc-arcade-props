DROP TABLE IF EXISTS display;


CREATE TABLE media
(
    id         SERIAL PRIMARY KEY,
    url        VARCHAR(255) NOT NULL,
    -- timestamps
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE display
(
    -- id database
    id          SERIAL PRIMARY KEY,
    -- player 1
    p1_name     VARCHAR(10),
    p1_media_id SERIAL    REFERENCES media (id) ON DELETE SET NULL,
    p1_score    INT,
    -- player 2
    p2_name     VARCHAR(10),
    p2_media_id SERIAL    REFERENCES media (id) ON DELETE SET NULL,
    p2_score    INT,
    -- feedback
    feedback    TEXT,
    -- timestamps
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER touch_media_updated_at
    AFTER UPDATE ON media
FOR EACH ROW
    WHEN (OLD.updated_at < CURRENT_TIMESTAMP) --- this avoid infinite loop
BEGIN
    UPDATE media SET updated_at=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TRIGGER touch_display_updated_at
    AFTER UPDATE ON media
    FOR EACH ROW
    WHEN (OLD.updated_at < CURRENT_TIMESTAMP) --- this avoid infinite loop
BEGIN
    UPDATE media SET updated_at=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;