-- @testpoint: 使用别名int4

drop table if exists integer14;
create table integer14 (name int4);
insert into integer14 values (122);
insert into integer14 values (123.456);
insert into integer14 values (0.000000009);
insert into integer14 values (-122);
insert into integer14 values (-99999.99999);
insert into integer14 values (-0.12355678);
select * from integer14;
drop table integer14;