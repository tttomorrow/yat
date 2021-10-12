-- @testpoint: 不指定精度，插入整数

drop table if exists float03;
create table float03 (name float);
insert into float03 values (12122);
insert into float03 values (-12122);
insert into float03 values (000009);
insert into float03 values (-98652171);
select * from float03;
drop table float03;
