--  @testpoint:插入左边界范围外整数值，应该报错：超出范围
drop table if exists bigint07;
create table bigint07 (name bigint);
select * from bigint07;
drop table if exists bigint07;