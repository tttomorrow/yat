-- @testpoint: setup 创建表
DROP TABLE IF EXISTS META_ENUM;
CREATE TABLE IF NOT EXISTS META_ENUM 
(ID BIGINT NOT NULL,
 ATTR_ID BIGINT NULL,
 NAME VARCHAR(60) NOT NULL,
   VALUE_LIST VARCHAR(1000),
   I18N_LIST VARCHAR(2000),
   PRIMARY KEY (ID))
;
DROP TABLE META_ENUM;
