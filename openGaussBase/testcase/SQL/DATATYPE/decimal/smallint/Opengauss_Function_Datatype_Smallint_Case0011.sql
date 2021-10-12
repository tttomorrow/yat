-- @testpoint: 插入bool类型

drop table if exists smallint11;
create table smallint11 (name smallint);
insert into smallint11 values (false);
insert into smallint11 values (true);
select * from smallint11;
drop table smallint11;