-- @testpoint: 创建列类型为货币类型的表，值大小超过bigint边界时合理报错
drop table if exists table_1;
create table table_1(price money);
insert into table_1 values(0.00);
drop table if exists table_1;