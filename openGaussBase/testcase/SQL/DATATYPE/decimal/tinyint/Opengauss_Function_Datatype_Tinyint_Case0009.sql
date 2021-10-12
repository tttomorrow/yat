-- @testpoint: 插入右边界范围值

drop table if exists tinyint09;
create table tinyint09 (name tinyint);
insert into tinyint09 values (255);
select * from tinyint09;
drop table tinyint09;