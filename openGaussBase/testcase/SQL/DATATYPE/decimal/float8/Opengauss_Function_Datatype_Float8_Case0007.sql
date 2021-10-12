-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists float8_07;
create table float8_07 (name float8);
insert into float8_07 values (1E+309);
drop table float8_07;