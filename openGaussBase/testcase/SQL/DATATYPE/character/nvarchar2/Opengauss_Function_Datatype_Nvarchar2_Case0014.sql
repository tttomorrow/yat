-- @testpoint: 插入特殊字符
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_14;
create table test_nvarchar2_14 (name nvarchar2(20));
insert into test_nvarchar2_14 values ('$@#%……&*（)');
select * from test_nvarchar2_14;
drop table test_nvarchar2_14;