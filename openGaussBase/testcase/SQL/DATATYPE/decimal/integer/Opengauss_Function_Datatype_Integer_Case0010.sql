-- @testpoint: 插入正整数

drop table if exists integer10;
create table integer10 (name integer);
insert into integer10 values (1223340);
insert into integer10 values (99999999);
insert into integer10 values (1);
insert into integer10 values (2);
insert into integer10 values (3);
select * from integer10;
drop table integer10;