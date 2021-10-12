-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists smallint02;
create table smallint02 (name smallint);
insert into smallint02 values (-32769);
drop table smallint02;