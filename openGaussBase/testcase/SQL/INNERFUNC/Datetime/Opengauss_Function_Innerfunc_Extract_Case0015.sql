--  @testpoint: EXTRACT 时间格式为INTERVAl月数超过12除以10
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL);
insert into test_date01 values ('25 months');
select EXTRACT(DECADE FROM clo1) from test_date01;
SELECT EXTRACT(DECADE FROM INTERVAL '25 months');
drop table if exists test_date01;