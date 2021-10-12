-- @testpoint: 插入0值

drop table if exists test_money04;
create table test_money04 (name money);
insert into test_money04 values (0);
insert into test_money04 values (0);
insert into test_money04 values (0);
select * from test_money04;
drop table test_money04;