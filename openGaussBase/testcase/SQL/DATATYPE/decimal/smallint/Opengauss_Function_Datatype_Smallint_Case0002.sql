-- @testpoint: 插入负整数

drop table if exists smallint02;
create table smallint02 (name smallint);
insert into smallint02 values (-1220);
insert into smallint02 values (-11111);
insert into smallint02 values (-1);
insert into smallint02 values (-2);
insert into smallint02 values (-3);
select * from smallint02;
drop table smallint02;