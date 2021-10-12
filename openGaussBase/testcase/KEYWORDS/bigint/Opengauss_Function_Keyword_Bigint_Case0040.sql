--  @testpoint:插入小数
drop table if exists bigint03;
create table bigint03 (name bigint);
insert into bigint03 values (122.3340);
select * from bigint03;
drop table if exists bigint03;
