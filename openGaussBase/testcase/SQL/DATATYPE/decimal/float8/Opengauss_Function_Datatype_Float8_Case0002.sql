-- @testpoint: 插入负浮点数

drop table if exists float8_02;
create table float8_02 (name float8);
insert into float8_02 values (-1212.5);
insert into float8_02 values (-99999.99999);
insert into float8_02 values (-0.000001);
select * from float8_02;
drop table float8_02;
