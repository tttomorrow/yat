-- @testpoint: 输入边界值

drop table if exists test_time01;
create table test_time01 (name time);
insert into test_time01 values ('00:00:00');
insert into test_time01 values ('23:59:59');
select * from test_time01;
drop table test_time01;