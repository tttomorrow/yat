-- @testpoint: 同一字段同时修改为not null和null，合理报错



drop table if exists test cascade;
create table test(id int);
alter table test modify (id not null, id null);
drop table if exists test cascade;



