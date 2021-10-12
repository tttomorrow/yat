-- @testpoint: 插入正常值

drop table if exists test_nvarchar2_01;
create table test_nvarchar2_01 (name nvarchar2(20));
insert into test_nvarchar2_01 values ('abcdefgh');
select * from test_nvarchar2_01;
drop table test_nvarchar2_01;