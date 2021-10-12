-- @testpoint: create 结合if not exists 使用
DROP TABLE IF EXISTS s_longtext;
CREATE TABLE IF not EXISTS s_longtext
(id                      NUMBER(7)
   CONSTRAINT s_longtext_id_nn NOT NULL,
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
  );
insert into s_longtext values(1,'李','小龙','截拳道大师');

drop table if exists lesli;
create table lesli as select text as text from s_longtext;
select * from lesli;
drop table if exists lesli;
DROP TABLE IF EXISTS s_longtext;
 
