-- @testpoint: create table与 with 子句（VERSION），非dfs表合理报错
DROP TABLE IF EXISTS tab_17;
CREATE TABLE tab_17
(id               NUMBER(7),
 name              VARCHAR2(20)
  )with(VERSION=0.12);
DROP TABLE IF EXISTS tab_17;

