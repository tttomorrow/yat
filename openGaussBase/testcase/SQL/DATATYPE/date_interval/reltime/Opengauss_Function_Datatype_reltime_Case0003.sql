-- @testpoint: 相对时间间隔类型reltime,插入空值

drop table if exists reltime03;
create table reltime03 (id int,name reltime);
insert into reltime03 values (1,'');
insert into reltime03 values (2,null);
select * from reltime03;
drop table reltime03;
