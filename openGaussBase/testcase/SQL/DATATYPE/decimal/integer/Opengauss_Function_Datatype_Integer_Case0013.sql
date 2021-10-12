-- @testpoint: 插入空值

drop table if exists integer13;
create table integer13 (id dec,name integer);
insert into integer13 values (1,'');
insert into integer13 values (1,null);
select * from integer13;
drop table integer13;