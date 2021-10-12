-- @testpoint: 插入正常范围值

drop table if exists test_varchar2_02;
create table test_varchar2_02 (name varchar2(20));
insert into test_varchar2_02 values ('abcdefgh');
select * from test_varchar2_02;
drop table test_varchar2_02;
