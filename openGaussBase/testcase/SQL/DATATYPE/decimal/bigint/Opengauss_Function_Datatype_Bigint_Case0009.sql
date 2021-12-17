-- @testpoint: 插入右边界范围值

drop table if exists bigint09;
create table bigint09 (name bigint);
insert into bigint09 values (9223372036854775807);
select * from bigint09;
drop table bigint09;