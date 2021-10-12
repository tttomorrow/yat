-- @testpoint: create table和LIKE INCLUDING CONSTRAINTS参数结合使用,插入数据违背check时合理报错

DROP TABLE IF EXISTS tab_12;
drop table if exists long;
CREATE TABLE tab_12
(id                     NUMBER(7)check(id>0),
 use_filename              VARCHAR2(20) ,
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
 );
insert into tab_12 values(10,'zhang','gongfu','大师');
insert into tab_12 values(0,'zhang','gongfu','大师');
insert into tab_12 values(-10,'zhang','gongfu','大师');
select * from tab_12;
create table long (like  tab_12 INCLUDING CONSTRAINTS);
insert into long values(0,'wanh','ni','大lao师');
select * from long;
drop table if exists tab_12;
drop table if exists long;