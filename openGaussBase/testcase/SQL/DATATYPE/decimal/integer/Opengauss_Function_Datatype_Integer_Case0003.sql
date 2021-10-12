-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists integer03;
create table integer03 (name integer);
drop table integer03;