-- @testpoint: 创建列类型是tinyint表，超出边界时合理报错
drop table if exists table_1;
create table table_1(a TINYINT);
insert into table_1 values(0);
insert into table_1 values(125);
insert into table_1 values(225);
--ERROR:  tinyint out of range
insert into table_1 values(-1);
insert into table_1 values(256);
select * from table_1;
drop table if exists table_1;
