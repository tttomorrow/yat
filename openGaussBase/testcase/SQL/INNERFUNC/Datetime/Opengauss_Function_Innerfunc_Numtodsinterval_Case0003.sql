--  @testpoint: numtodsinterval interval_unit为 ’MINUTE‘
drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('2001-02-16');
select to_date(clo1) + numtodsinterval(100, 'MINUTE') from test_date01;
SELECT numtodsinterval(100, 'MINUTE');
drop table if exists test_date01;