-- @testpoint: 创建列类型为整数类型INT2,插入数据超过边界时合理报错
drop table if exists table_1;
create table table_1(a INT2);
insert into table_1 values(-32768);
insert into table_1 values(12553);
insert into table_1 values(32767);

insert into table_1 values(-32769);
insert into table_1 values(32768);
select * from table_1;
drop table if exists table_1;