-- @testpoint: 插入右边界范围值

drop table if exists smallint09;
create table smallint09 (name smallint);
insert into smallint09 values (32767);
select * from smallint09;
drop table smallint09;