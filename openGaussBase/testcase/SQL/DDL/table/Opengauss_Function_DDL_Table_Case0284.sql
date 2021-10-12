-- @testpoint: 同一字段同时修改类型，合理报错




--修改同一字段为相同类型int两次
drop table if exists test cascade;
create table test(id int);
alter table test modify (id int, id int);
drop table if exists test cascade;


--实际：修改成功





--修改同一字段为不同类型两次
drop table if exists test cascade;
create table test(id int);
alter table test modify (id int, id char);
drop table if exists test cascade;


--实际：修改成功



--修改同一字段相同类型不同长度
drop table if exists test cascade;
create table test(id char);
alter table test modify (id char(20), id char(30));
drop table if exists test cascade;

--实际，合理报错提示