-- @testpoint: 创建列类型为字符类型char、CHARACTER(n)、NCHAR(n)的表，插入数据超过n时合理报错
drop table if exists table_1;
create table table_1(a char(20));
insert into table_1 values('zhangxiaox');
insert into table_1 values('张三');
insert into table_1 values('qwertyuiopqwe');
select * from table_1;
drop table if exists table_1;

drop table if exists table_2;
create table table_2(a character(10));
insert into table_2 values('zhangxiaox');
insert into table_2 values('张三');

insert into table_2 values('qwertyuiopqwe');
select * from table_2;
drop table if exists table_2;

drop table if exists table_3;
create table table_3(a nchar);
insert into table_3 values('z');

insert into table_3 values('张');
insert into table_3 values('qwertyu');
select * from table_3;
drop table if exists table_3;