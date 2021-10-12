-- @testpoint: 创建带非空约束的表(表级合理报错)

DROP TABLE IF EXISTS tab_12;

CREATE TABLE tab_12
(id                      NUMBER(7),
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000), not null(id);
