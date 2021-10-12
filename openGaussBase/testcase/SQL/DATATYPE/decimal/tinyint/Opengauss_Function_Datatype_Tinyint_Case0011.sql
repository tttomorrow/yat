-- @testpoint: 插入bool类型

drop table if exists tinyint11;
create table tinyint11 (name tinyint);
insert into tinyint11 values (false);
insert into tinyint11 values (true);
select * from tinyint11;
drop table tinyint11;