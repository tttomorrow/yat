--  @testpoint: numtodsinterval interval_unit? 扢INUTE??????

drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('2001-02-16');
SET intervalstyle = a;
SELECT numtodsinterval(100, 'MINUTE');
select to_date(clo1) + numtodsinterval(100, 'MINUTE') from test_date01;
drop table if exists test_date01;