-- @testpoint: 给定参数超过固定参数个数，合理报错
drop table if exists tbc;
create table tbc
(
id integer,
name char(50),
sex char(50)
);
create index tbc_index on tbc(id);
insert into tbc values(1,'wang','male');
insert into tbc values(2,'zhang','female');
select sex,count(1,2) from tbc group by sex order by 1;
drop table if exists tbc;