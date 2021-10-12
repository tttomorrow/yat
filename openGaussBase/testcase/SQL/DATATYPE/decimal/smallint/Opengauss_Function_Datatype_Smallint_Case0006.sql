-- @testpoint: 插入左边界范围值

drop table if exists smallint06;
create table smallint06 (name smallint);
insert into smallint06 values (-32768);
select * from smallint06;
drop table smallint06;
