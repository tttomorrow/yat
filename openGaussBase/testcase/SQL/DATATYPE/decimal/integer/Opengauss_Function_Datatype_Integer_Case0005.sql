-- @testpoint: 插入字符串类型数值

drop table if exists integer05;
create table integer05 (name integer);
insert into integer05 values ('123456');
insert into integer05 values ('99999999');
insert into integer05 values ('-12356');
insert into integer05 values ('-99999999');
select * from integer05;
drop table integer05;