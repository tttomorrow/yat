-- @testpoint: 创建一个表user_02，定义user列不带引号,合理报错

drop table if  exists user_02;
CREATE TABLE user_02 (name varchar(13),school varchar(13),USER INT);