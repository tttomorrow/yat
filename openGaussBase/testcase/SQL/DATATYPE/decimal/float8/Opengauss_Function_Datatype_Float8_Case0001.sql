-- @testpoint: 插入正浮点数

drop table if exists float8_01;
create table float8_01 (name float8);
insert into float8_01 values (120.123);
insert into float8_01 values (99999.99999);
insert into float8_01 values (0.000001);
select * from float8_01;
drop table float8_01;