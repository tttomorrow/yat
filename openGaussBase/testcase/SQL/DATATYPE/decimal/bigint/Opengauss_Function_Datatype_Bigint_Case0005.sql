-- @testpoint: 插入特殊字符，合理报错

drop table if exists bigint05;
create table bigint05 (name bigint);
insert into bigint05 values (!@#$%……&);
drop table bigint05;