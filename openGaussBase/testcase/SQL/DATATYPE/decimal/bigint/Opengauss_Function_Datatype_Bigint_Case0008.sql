-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists bigint06;
create table bigint06 (name bigint);
select * from bigint06;
drop table bigint06;
