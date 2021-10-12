-- @testpoint: max函数与where和order by联用
drop table if exists test1;
create table test1(cust_id int4, time_id DATE);
insert into test1 values(12, '2019-02-05 00:37:00');
insert into test1 values(32, '2022-02-05 23:00:59');
insert into test1 values(39, '1012-02-05 01:00:00');
insert into test1 values(1, '2019-02-05 00:37:00');
insert into test1 values(2, '2022-02-05 23:00:59');
insert into test1 values(3, '1012-02-05 01:00:00');
select max(time_id) from test1 where cust_id >0 order by 1;
drop table if exists test1;