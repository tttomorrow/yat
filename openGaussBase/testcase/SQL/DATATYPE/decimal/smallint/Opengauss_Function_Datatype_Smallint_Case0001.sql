-- @testpoint: 插入正整数

drop table if exists smallint01;
create table smallint01 (name smallint);
insert into smallint01 values (120);
insert into smallint01 values (11111);
insert into smallint01 values (1);
insert into smallint01 values (2);
insert into smallint01 values (3);
select * from smallint01;
drop table smallint01;