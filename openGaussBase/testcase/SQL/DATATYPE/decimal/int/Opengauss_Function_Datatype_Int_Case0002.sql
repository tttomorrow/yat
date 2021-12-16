-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists int02;
create table int02 (name int);
insert into int02 values (-2147483649);
drop table int02;