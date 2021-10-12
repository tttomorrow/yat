-- @testpoint: 插入0值

drop table if exists smallint14;
create table smallint14 (name smallint);
insert into smallint14 values (0);
insert into smallint14 values (0);
insert into smallint14 values (0);
select * from smallint14;
drop table smallint14;