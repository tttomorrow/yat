-- @testpoint: 插入左边界范围值

drop table if exists int01;
create table int01 (name int);
insert into int01 values (-2147483648);
select * from int01;
drop table int01;