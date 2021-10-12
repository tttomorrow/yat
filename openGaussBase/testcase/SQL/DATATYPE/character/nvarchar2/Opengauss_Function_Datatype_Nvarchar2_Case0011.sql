-- @testpoint: 插入布尔值
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_11;
create table test_nvarchar2_11 (name nvarchar2(20));
insert into test_nvarchar2_11 values (true);
insert into test_nvarchar2_11 values (false);
select * from test_nvarchar2_11;
drop table test_nvarchar2_11;