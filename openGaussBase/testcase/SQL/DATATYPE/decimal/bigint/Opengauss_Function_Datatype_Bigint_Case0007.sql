-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists bigint06;
create table bigint06 (name bigint);
insert into bigint06 values (-9223372036854775809);
drop table bigint06;