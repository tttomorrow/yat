-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists integer02;
create table integer02 (name integer);
drop table integer02;