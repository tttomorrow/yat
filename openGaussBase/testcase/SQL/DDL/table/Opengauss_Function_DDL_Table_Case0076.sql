-- @testpoint: 创建表设置(列级)外键，外键不支持，合理报错

DROP TABLE IF EXISTS tab_11;

CREATE TABLE tab_11
(id                     NUMBER(7) foreign key,
 use_filename              VARCHAR2(20) ,
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
 );

drop table if exists tab_11;
