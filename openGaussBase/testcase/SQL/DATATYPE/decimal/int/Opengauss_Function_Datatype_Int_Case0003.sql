-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists int03;
create table int03 (name int);
insert into int03 values (2147483648);
drop table int03;