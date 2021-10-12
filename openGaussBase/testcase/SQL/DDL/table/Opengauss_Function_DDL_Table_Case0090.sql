-- @testpoint: 创建带DEFAULT约束的表(列级),默认值和数据类型匹配

DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id             int  DEFAULT '123',
name              VARCHAR2(20),
filename          VARCHAR2(255),
text               VARCHAR2(2000)
 );
insert into  tab_12 values(1,'zhang','text','hahahahah');
insert into  tab_12 values(100,'zhang','text','hahahahah');
insert into  tab_12 (name,filename,text )  values('zhang','text','hahahahah');
select *from tab_12;
drop table if exists tab_12;