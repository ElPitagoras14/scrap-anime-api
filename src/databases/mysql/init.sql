CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password CHAR(60) NOT NULL,
    profile_img VARCHAR(255),
    is_admin BOOL NOT NULL DEFAULT FALSE,
    is_active BOOL NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE animes (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_src VARCHAR(255) NOT NULL,
    is_finished BOOL NOT NULL DEFAULT TRUE,
    week_day VARCHAR(32),
    last_peek DATETIME NOT NULL
);

CREATE TABLE episodes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    anime_id VARCHAR(255) NOT NULL,
    episode_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    CONSTRAINT fk_episode_anime FOREIGN KEY (anime_id) REFERENCES animes (id)
);

CREATE TABLE user_save_anime (
    user_id CHAR(36),
    anime_id VARCHAR(255),
    PRIMARY KEY (user_id, anime_id),
    CONSTRAINT fk_user_save FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_anime_save FOREIGN KEY (anime_id) REFERENCES animes (id)
);