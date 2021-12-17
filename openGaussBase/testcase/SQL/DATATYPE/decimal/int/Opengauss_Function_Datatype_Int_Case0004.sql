-- @testpoint: 插入右边界范围值

drop table if exists int04;
create table int04 (name int);
insert into int04 values (2147483647);
select * from int04;
drop table int04;