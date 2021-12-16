-- @testpoint: 创建列类型为货币类型的表，值大小超过bigint边界时合理报错
drop table if exists table_1;
create table table_1(price money);
insert into table_1 values(-92233720368547758.08);
insert into table_1 values(-92233720368547758.08);
insert into table_1 values(42233720368547758.369);
insert into table_1 values(0.00);
insert into table_1 values(92233720368547758.07);
insert into table_1 values(-92233720368547758.09);
insert into table_1 values(92233720368547758.08);
drop table if exists table_1;