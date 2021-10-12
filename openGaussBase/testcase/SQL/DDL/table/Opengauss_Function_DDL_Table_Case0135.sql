-- @testpoint: 创建列类型为二进制类型blob的表
drop table if exists table_2;
create table table_2(a BLOB);
insert into table_2 values(empty_blob());
select * from table_2;
drop table if exists table_2;