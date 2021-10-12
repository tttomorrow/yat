-- @testpoint: 插入浮点数

drop table if exists smallint03;
create table smallint03 (name smallint);
insert into smallint03 values (122.3340);
insert into smallint03 values (0.000001);
insert into smallint03 values (-122.3340);
insert into smallint03 values (-0.000001);
select * from smallint03;
drop table smallint03;