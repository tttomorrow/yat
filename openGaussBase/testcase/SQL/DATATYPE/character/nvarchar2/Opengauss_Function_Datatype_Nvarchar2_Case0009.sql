-- @testpoint: 插入空格
-- @modified at: 2020-11-16

drop table if exists test_nvarchar2_09;
create table test_nvarchar2_09 (id int,name nvarchar2(20),title nvarchar2(20));
insert into test_nvarchar2_09 values (1,'  ','gkb中国');
insert into test_nvarchar2_09 values (2,'中国gkb','  ');
select * from test_nvarchar2_09;
drop table test_nvarchar2_09;