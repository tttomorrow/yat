-- @testpoint: 创建列类型是序列整型-BIGSERIAL的表，超边界时合理报错
drop table if exists table_1;
create table table_1(a BIGSERIAL);
insert into table_1 values(1);
insert into table_1 values(1255345657);
insert into table_1 values(9223372036854775807);

insert into table_1 values(0);
insert into table_1 values(9223372036854775808);
select * from table_1;
drop table if exists table_1;