-- @testpoint: 插入右边界范围值

drop table if exists integer04;
create table integer04 (name integer);
insert into integer04 values (2147483647);
select * from integer04;
drop table integer04;