-- @testpoint: 创建列类型为字符类型text的表,
drop table if exists table_2;
create table table_2(a TEXT);
insert into table_2 values('qwweerth');
insert into table_2 values(122);
select * from table_2;
drop table if exists table_2;