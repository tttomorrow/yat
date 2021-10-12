-- @testpoint: 插入汉字和英文

drop table if exists test_nvarchar2_08;
create table test_nvarchar2_08 (name nvarchar2(20));
insert into test_nvarchar2_08 values ('gkb中国');
insert into test_nvarchar2_08 values ('中国gkb');
select * from test_nvarchar2_08;
drop table if exists test_nvarchar2_08;