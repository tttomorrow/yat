--  @testpoint:插入负数
drop table if exists bigint02;
create table bigint02 (name bigint);
insert into bigint02 values (-1.5);
select * from bigint02;
drop table if exists bigint02;
