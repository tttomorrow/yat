-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists float8_06;
create table float8_06 (name float8);
insert into float8_06 values (1E-325);
drop table float8_06;
