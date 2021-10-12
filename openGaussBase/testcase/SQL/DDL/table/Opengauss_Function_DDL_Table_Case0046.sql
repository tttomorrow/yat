-- @testpoint: create 普通表
DROP TABLE IF EXISTS s_longtext;
CREATE TABLE s_longtext
(id                      NUMBER(7),
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
  );
insert into s_longtext values(1,'李','小龙','截拳道大师');
select * from s_longtext;
drop table if exists s_longtext;
