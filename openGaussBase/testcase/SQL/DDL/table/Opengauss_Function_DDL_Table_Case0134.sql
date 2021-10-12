-- @testpoint: 创建列类型为特殊字符类型name的表
drop table if exists table_2;
create table table_2(a name);
insert into table_2 values('qwweerth');
insert into table_2 values(122);
select * from table_2;
drop table if exists table_2;
