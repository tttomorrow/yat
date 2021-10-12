--  @testpoint: numtodsinterval interval_unit为 ’MINUTE‘小数
drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('2001-02-16');
select to_date(clo1) + numtodsinterval(100.001, 'MINUTE') from test_date01;
SELECT numtodsinterval(100.00000001, 'MINUTE');
drop table if exists test_date01;