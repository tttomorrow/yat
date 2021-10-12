--  @testpoint:插入正数
drop table if exists bigint01;
create table bigint01 (name bigint);
insert into bigint01 values (120);
select * from bigint01;
drop table if exists bigint01;