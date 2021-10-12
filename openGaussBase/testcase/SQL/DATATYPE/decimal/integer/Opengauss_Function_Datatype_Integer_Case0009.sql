-- @testpoint: 插入0值

drop table if exists integer09;
create table integer09 (name integer);
insert into integer09 values (0);
insert into integer09 values (0);
insert into integer09 values (0);
select * from integer09;
drop table integer09;