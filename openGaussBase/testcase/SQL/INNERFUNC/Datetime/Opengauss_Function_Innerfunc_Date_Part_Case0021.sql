-- @testpoint: date_part入参为采用数字表示的时间段
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('60');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', reltime '121');
drop table if exists test_date01;