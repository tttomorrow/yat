-- @testpoint: 缁撳悎case when

drop table if exists test_date03;
create table test_date03 (name date);
insert into test_date03 values ('2018-09-18');
insert into test_date03 values ('2018-09-15');
select case when date '2018-09-17' > date '2018-09-16' then 'A' else 'B' end;
drop table test_date03;