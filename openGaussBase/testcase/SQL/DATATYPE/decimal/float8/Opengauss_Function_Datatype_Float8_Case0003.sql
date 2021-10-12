-- @testpoint: 插入整数

drop table if exists float8_03;
create table float8_03 (name float8);
insert into float8_03 values (12122);
insert into float8_03 values (9999^2);
insert into float8_03 values (-12122);
insert into float8_03 values (-9999^2);
select * from float8_03;
drop table float8_03;
