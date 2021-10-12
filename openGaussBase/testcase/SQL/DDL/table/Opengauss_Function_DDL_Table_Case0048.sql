-- @testpoint: 创建列存表

DROP TABLE IF EXISTS s_longtext;
CREATE TABLE s_longtext
(id                      NUMBER(7)
   CONSTRAINT s_longtext_id_nn NOT NULL,
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
  )WITH (ORIENTATION = COLUMN);
insert into s_longtext values(1,'李','小龙','截拳道大师');
select * from s_longtext;
drop table if exists s_longtext;
