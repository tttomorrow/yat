--  @testpoint: justify_days 
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('31.25');
select justify_days(clo1) from test_date01;
SELECT justify_days(reltime  '31.25');
drop table if exists test_date01;