-- @testpoint: 创建相同表名的表,合理报错
DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id                      NUMBER(7)not null,
 text                       VARCHAR2(2000)
 );

--ERROR:  relation "tab_12" already exists
CREATE TABLE TAB_12
(id                      NUMBER(7)not null,
 text                       VARCHAR2(2000)
 );
--ERROR:  relation "tab_12" already exists
CREATE TABLE tab_12
(id                      NUMBER(7)not null,
 text                       VARCHAR2(2000)
 );
drop table if exists tab_12;
 
