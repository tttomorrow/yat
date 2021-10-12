--  @testpoint:插入正整数
drop table if exists bigint05;
create table bigint05 (name bigint);
insert into bigint05 values (1216561);
select * from bigint05;
drop table if exists bigint05;