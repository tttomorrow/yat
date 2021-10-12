-- @testpoint: 与group by、having语句联用验证count计数结果
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
insert into tbc values(3,'zhang','male');
insert into tbc values(4,'wang','female');
insert into tbc values(5,'sun');
insert into tbc values(6,'sun','male');

select count(*) from tbc;
select sex from tbc group by sex having count(1) is not null order by 1;
select sex from tbc group by sex having count(*) order by 1;
select name from tbc group by name having count(*) is not null order by 1;
drop table if exists tbc;