-- @testpoint: 创建列类型为二进制类型raw的表
drop table if exists table_2;
create table table_2(a RAW);
insert into table_2 values(HEXTORAW('DEADBEEF'));
select * from table_2;
drop table if exists table_2;