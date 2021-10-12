--  @testpoint: EXTRACT 时间格式为date(只有时分秒、有时区无时区、边界值)时取CENTURY
drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('0001-01-01 00:00:00');
insert into test_date01 values ('2001-01-01 pst');
insert into test_date01 values ('1998-01-01');
insert into test_date01 values ('1830-01-01 23:00:00 pst');
insert into test_date01 values ('2505-01-01 00:00:00+8');
select EXTRACT(CENTURY FROM clo1) from test_date01;
SELECT EXTRACT(CENTURY FROM date '0001-01-01 00:00:00');
SELECT EXTRACT(CENTURY FROM date '0101-01-01 00:00:00');
SELECT EXTRACT(CENTURY FROM date '0218-01-01 pst');
SELECT EXTRACT(CENTURY FROM date '1998-01-01');
SELECT EXTRACT(CENTURY FROM date '1830-01-01 23:00:00 pst');
SELECT EXTRACT(CENTURY FROM date '2505-01-01 00:00:00+8');
drop table if exists test_date01;