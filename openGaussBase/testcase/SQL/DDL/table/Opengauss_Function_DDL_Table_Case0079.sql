-- @testpoint: 创建一个有检查约束列的表(表级)，插入数据违背check时合理报错

DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id             int check(id>0),
name              VARCHAR2(20) ,
filename          VARCHAR2(255),
text               VARCHAR2(2000),
check(id>0)
 );
insert into  tab_12 values(1,'zhang','text','hahahahah');
insert into  tab_12 values(100,'zhang','text','hahahahah');
insert into  tab_12 values(-1,'zhang','text','hahahahah');
select *from tab_12;
drop table if exists tab_12;