-- @testpoint: td_compatible_truncation参数值为off，目标表中char和varchar类型超过限定字符长度不会截断，合理报错
--查看参数默认值
show td_compatible_truncation;
--建表
drop table if exists table1;
CREATE TABLE table1(id int, a char(6), b varchar(6),c varchar(6));
--插入数据，合理报错ERROR:  value too long for type character(6)
INSERT INTO table1 VALUES(1,reverse('123ＡＡ78'),reverse('123ＡＡ78'),reverse('123ＡＡ78'));
--删表
drop table if exists table1;
