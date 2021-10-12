-- @testpoint: 增加字段用默认值，defaul为null，并且有not null约束
DROP TABLE IF EXISTS META_ENUM;
CREATE TABLE IF NOT EXISTS META_ENUM(ID BIGINT NOT NULL,
 ATTR_ID BIGINT NULL,
 NAME VARCHAR(60) NOT NULL,
   VALUE_LIST VARCHAR(1000),
   I18N_LIST VARCHAR(2000),
   PRIMARY KEY (ID));
ALTER TABLE META_ENUM ADD  location6 VARCHAR(20) NOT NULL DEFAULT null;
ALTER TABLE META_ENUM ADD  location7 VARCHAR(20) DEFAULT null NOT NULL;
DROP TABLE META_ENUM;