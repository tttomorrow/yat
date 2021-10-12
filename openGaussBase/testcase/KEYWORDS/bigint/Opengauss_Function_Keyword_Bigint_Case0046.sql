--  @testpoint:插入右边界范围外整数，应该报错：超出范围
drop table if exists bigint09;
create table bigint09 (name bigint);
select * from bigint09;
drop table if exists bigint09;