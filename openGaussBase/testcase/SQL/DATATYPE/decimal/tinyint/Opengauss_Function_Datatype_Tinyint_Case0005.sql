-- @testpoint: 插入特殊字符,合理报错

drop table if exists tinyint05;
create table tinyint05 (name tinyint);
insert into tinyint05 values (@);
insert into tinyint05 values ('#');
drop table tinyint05;