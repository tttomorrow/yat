-- @testpoint: 插入bool类型，合理报错

drop table if exists float8_10;
create table float8_10 (name float8);
insert into float8_10 values (false);
insert into float8_10 values (true);
drop table float8_10;