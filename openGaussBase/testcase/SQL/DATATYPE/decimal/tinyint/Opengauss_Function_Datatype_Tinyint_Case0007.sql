-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists tinyint07;
create table tinyint07 (name tinyint);
insert into tinyint07 values (-1);
drop table tinyint07;
