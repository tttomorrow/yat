-- @testpoint: 插入左边界范围值

drop table if exists tinyint06;
create table tinyint06 (name tinyint);
insert into tinyint06 values (0);
select * from tinyint06;
drop table tinyint06;
