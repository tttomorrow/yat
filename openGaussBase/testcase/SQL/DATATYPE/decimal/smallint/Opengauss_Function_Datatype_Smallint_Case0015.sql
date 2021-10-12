-- @testpoint: 使用别名int2

drop table if exists smallint15;
create table smallint15 (name int2);
insert into smallint15 values (121);
insert into smallint15 values (11111);
insert into smallint15 values (1);
insert into smallint15 values (2);
insert into smallint15 values (3);
select * from smallint15;
drop table smallint15;