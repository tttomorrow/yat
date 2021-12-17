-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists integer02;
create table integer02 (name integer);
insert into integer02 values (-2147483649);
drop table integer02;