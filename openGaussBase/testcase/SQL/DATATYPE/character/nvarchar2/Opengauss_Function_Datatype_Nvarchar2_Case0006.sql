-- @testpoint: 插入空值
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_06;
create table test_nvarchar2_06 (id int,name nvarchar2(8));
insert into test_nvarchar2_06 values (1,'');
insert into test_nvarchar2_06 values (1,null);
select * from test_nvarchar2_06;
drop table test_nvarchar2_06;