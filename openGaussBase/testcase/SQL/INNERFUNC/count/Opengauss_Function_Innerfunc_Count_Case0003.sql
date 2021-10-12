-- @testpoint: 异常校验，合理报错
drop table if exists tbc;
create table tbc
(
id integer,
name char(10),
sex char(10)
);
create index tbc_index on tbc(id);
insert into tbc values(1,'wang','male');
insert into tbc values(2,'zhang','female');
insert into tbc values(5,'sun');
select * from tbc;
select count() from tbc;
select count('') from tbc;
select count(null) from tbc;
select count(none) from tbc;
select count('f') from tbc;
select count('男') from tbc;
drop table if exists tbc;