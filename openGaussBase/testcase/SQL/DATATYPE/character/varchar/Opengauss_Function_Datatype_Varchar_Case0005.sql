-- @testpoint: 插入正常值，字节长度设定为1
-- @modify at: 2020-11-17

drop table if exists test_varchar_05;
create table test_varchar_05 (name varchar(1));
insert into test_varchar_05 values ('a');
select * from test_varchar_05;
drop table test_varchar_05;