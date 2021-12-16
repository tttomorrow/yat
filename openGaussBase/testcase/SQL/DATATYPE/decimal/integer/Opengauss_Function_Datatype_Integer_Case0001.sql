-- @testpoint: 插入左边界范围值

drop table if exists integer01;
create table integer01 (name integer);
insert into integer01 values (-2147483648);
select * from integer01;
drop table integer01;