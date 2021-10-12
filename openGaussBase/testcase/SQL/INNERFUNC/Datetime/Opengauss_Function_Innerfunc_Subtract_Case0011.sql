-- @testpoint: timestamp不带时区相减
drop table if exists test_date01;
create table test_date01 (col1 timestamp without time zone);
insert into test_date01 values ('2003-04-12 04:59:00');
select col1 - time '19:01'   from test_date01;
drop table if exists test_date01;