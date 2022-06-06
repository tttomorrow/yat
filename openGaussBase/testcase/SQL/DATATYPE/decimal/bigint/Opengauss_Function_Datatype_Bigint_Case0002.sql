-- @testpoint: 插入有效负整数

drop table if exists bigint02;
create table bigint02 (name bigint);
insert into bigint02 values (-102);
insert into bigint02 values (-9999999);
insert into bigint02 values (-2233445566);
select * from bigint02;
drop table bigint02;
