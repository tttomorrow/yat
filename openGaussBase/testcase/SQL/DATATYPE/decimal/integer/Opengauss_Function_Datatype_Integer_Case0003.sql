-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists integer03;
create table integer03 (name integer);
insert into integer03 values (2147483648);
drop table integer03;