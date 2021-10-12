-- @testpoint: 创建列类型为字符类型VARCHAR(n)、CHARACTER VARYING(n)的表，插入数据超过n时合理报错
drop table if exists table_1;
create table table_1(a varchar(20));
insert into table_1 values('zhangxiaox');
insert into table_1 values('张三');
insert into table_1 values('qwertyuiopqwe');
select * from table_1;
drop table if exists table_1;

drop table if exists table_2;
create table table_2(a character varying(10));
insert into table_2 values('zhangxiaox');
insert into table_2 values('张三');
--ERROR:  value too long for type character(10)
insert into table_2 values('qwertyuiopqwe');
select * from table_2;
drop table if exists table_2;

