-- @testpoint: 插入非法空值,合理报错

drop table if exists tinyint13;
create table tinyint13 (id int,name tinyint);
insert into tinyint13 values (1,' ');
drop table tinyint13;