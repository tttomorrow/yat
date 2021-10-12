-- @testpoint: 创建带DEFAULT约束的表(表级合理报错)
DROP TABLE IF EXISTS tab_11;
--ERROR:  syntax error at or near "DEFAULT"
CREATE TABLE tab_11
(id                     NUMBER(7) ,
 use_filename              VARCHAR2(20) ,
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000),
 default 'aaa' (filename)
 );


