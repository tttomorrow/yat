-- @testpoint: 插入0值

drop table if exists float8_13;
create table float8_13 (name float8);
insert into float8_13 values (0);
insert into float8_13 values (0);
insert into float8_13 values (0);
select * from float8_13;
drop table float8_13;