-- @testpoint: create table和LIKE INCLUDING DEFAULTS参数结合使用

DROP TABLE IF EXISTS tab_11;
drop table if exists long;
CREATE TABLE tab_11
(id                     NUMBER(7),
 use_filename              VARCHAR2(20) ,
 filename                  VARCHAR2(255)default 'test01',
 text                       VARCHAR2(2000)
 );
insert into tab_11(id,use_filename,text ) values(1,'zhang','大师');
select * from tab_11;
create table long (like  tab_11 INCLUDING DEFAULTS);
insert into long(id,use_filename,text ) values(3,'wanh','大lao师');
select * from long;
drop table if exists tab_11;
drop table if exists long;
