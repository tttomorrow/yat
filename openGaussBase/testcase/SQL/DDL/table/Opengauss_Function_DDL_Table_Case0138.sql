-- @testpoint: 创建列类型为整数类型INT1,插入数据超过边界时合理报错
drop table if exists table_2;
create table table_2(a INT1);
insert into table_2 values(0);
insert into table_2 values(125);
insert into table_2 values(255);
insert into table_2 values(-1);
insert into table_2 values(256);
select * from table_2;
drop table if exists table_2;