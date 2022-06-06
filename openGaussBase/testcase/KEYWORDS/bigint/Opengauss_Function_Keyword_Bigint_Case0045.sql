--  @testpoint:插入右边界范围值，未超出范围
drop table if exists bigint08;
create table bigint08 (name bigint);
insert into bigint08 values (9223372036854775807 );
select * from bigint08;
drop table if exists bigint08;