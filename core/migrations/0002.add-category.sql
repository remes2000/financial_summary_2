CREATE TABLE category (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(512) NOT NULL UNIQUE
);

CREATE TABLE regular_expression (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    category_id BIGINT NOT NULL,
    content VARCHAR(512) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

ALTER TABLE account_transaction ADD COLUMN category_id BIGINT;
ALTER TABLE account_transaction ADD FOREIGN KEY (category_id) REFERENCES category(id);