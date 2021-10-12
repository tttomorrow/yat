-- @testpoint: 创建带非空约束的表(列级)，在插入数据为空时合理报错

DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id                      NUMBER(7)not null,
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000));
insert into tab_12 values(1,'李','小龙','截拳道大师');
insert into tab_12 (use_filename,filename,text)values('李','小龙','截拳道大师');
select * from  tab_12;
drop table if exists tab_12;