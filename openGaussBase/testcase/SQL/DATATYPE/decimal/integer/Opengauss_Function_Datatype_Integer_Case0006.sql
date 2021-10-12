-- @testpoint: 插入bool类型

drop table if exists integer06;
create table integer06 (name integer);
insert into integer06 values (false);
insert into integer06 values (true);
select * from integer06;
drop table integer06;