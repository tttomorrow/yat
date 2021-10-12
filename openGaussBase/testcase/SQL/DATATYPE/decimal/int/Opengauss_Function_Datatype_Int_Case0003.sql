-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists int03;
create table int03 (name int);
drop table int03;