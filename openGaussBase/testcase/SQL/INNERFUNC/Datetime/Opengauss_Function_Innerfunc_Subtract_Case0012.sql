-- @testpoint: time类型相减
drop table if exists test_date01;
create table test_date01 (col1 time);
insert into test_date01 values ('04:59:59');
select time '04:59:59' - time '04:59:59'    from test_date01;
drop table if exists test_date01;