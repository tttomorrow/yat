-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists tinyint08;
create table tinyint08 (name tinyint);
insert into tinyint08 values (256);
drop table tinyint08;
