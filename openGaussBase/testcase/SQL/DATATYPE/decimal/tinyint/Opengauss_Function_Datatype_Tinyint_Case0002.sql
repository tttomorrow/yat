-- @testpoint: 插入负整数，合理报错

drop table if exists tinyint02;
create table tinyint02 (name tinyint);
insert into tinyint02 values (-15);
insert into tinyint02 values (-1);
insert into tinyint02 values (-2);
insert into tinyint02 values (-3);
drop table tinyint02;
