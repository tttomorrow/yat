-- @testpoint: EXTRACT 时间格式为INTERVAL只包含天数部分，除以10
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL);
insert into test_date01 values ('12.5 days');
select EXTRACT(DECADE FROM clo1) from test_date01;
SELECT EXTRACT(DECADE FROM INTERVAL '12.5 days');
drop table if exists test_date01;