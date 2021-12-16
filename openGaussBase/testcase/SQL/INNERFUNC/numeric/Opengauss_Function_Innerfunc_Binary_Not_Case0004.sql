-- @testpoint: 数字操作符~(二进制NOT), 边界值进行二进制not
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (-9223372036854775808, 9223372036854775807);
select ~clo1, ~clo2 from data_01;
drop table if exists data_01;