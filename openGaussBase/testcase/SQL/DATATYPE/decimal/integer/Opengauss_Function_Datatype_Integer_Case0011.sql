-- @testpoint: 插入负整数

drop table if exists integer11;
create table integer11 (name integer);
insert into integer11 values (-1223340);
insert into integer11 values (-99999999);
insert into integer11 values (-1);
insert into integer11 values (-2);
insert into integer11 values (-3);
select * from integer11;
drop table integer11;