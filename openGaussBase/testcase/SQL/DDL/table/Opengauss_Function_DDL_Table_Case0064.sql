-- @testpoint: create table 与 with 子句（FILLFACTOR）
DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id                      NUMBER(7)
   CONSTRAINT tab_12_id_nn NOT NULL,
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
  )with(FILLFACTOR=70);
insert into tab_12 values(1,'李','小龙','截拳道大师');

drop table if exists tab_12;


 
