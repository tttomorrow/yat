-- @testpoint: 插入数值型值
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_10;
create table test_nvarchar2_10 (name nvarchar2(20));
insert into test_nvarchar2_10 values (88);
select * from test_nvarchar2_10;
drop table test_nvarchar2_10;