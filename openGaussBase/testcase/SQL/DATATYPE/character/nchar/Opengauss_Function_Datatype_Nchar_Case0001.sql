-- @testpoint: 字节长度设为0，合理报错
-- @modified at: 2020-11-16

DROP TABLE IF EXISTS type_nchar_01;
CREATE TABLE type_nchar_01 (stringv nchar(0));
