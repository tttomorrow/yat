-- @testpoint: 插入正常范围值，字节长度设定为1
-- @modify at: 2020-11-17

drop table if exists test_varchar2_04;
create table test_varchar2_04 (name varchar2(1));
insert into test_varchar2_04 values ('a');
select * from test_varchar2_04;
drop table test_varchar2_04;