-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists smallint08;
create table smallint08 (name smallint);
insert into smallint08 values (32768);
drop table smallint08;