--  @testpoint:插入左边界范围值，未超出范围
drop table if exists bigint06;
create table bigint06 (name bigint);
insert into bigint06 values (-9223372036854775808 );
select * from bigint06;
drop table if exists bigint06;
