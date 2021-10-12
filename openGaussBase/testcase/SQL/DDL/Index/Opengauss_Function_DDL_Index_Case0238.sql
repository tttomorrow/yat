-- @testpoint: 创建唯一索引后更新数据,合理报错

--1.创建表
create table test_238(i int, c char(5));
--2.创建唯一索引
create unique index unique_idx on test_238(i,c);
--3.插入数据，无重复值
INSERT INTO test_238 values (generate_series(1,200), 're');
--4.更新数据，具有重复值
update test_238 set i = 2001 where i>10;
--5.更新数据，无重复值
update test_238 set i = 2001 where i=10;
--6.查询
explain select * from test_238 where i>197;
--7.删除索引
drop index unique_idx;
--8.更新数据
update test_238 set i = 2001 where i=11;
--9.创建唯一索引
create unique index unique_idx on test_238(i,c);
--10.修改重复值
delete from test_238 where i = 2001;
--11.创建唯一索引
create unique index unique_idx on test_238(i,c);
--12.更新数据
update test_238 set i = 2 where i=1;
--13.插入数据
INSERT INTO test_238 values (1234, 're');

--tearDown
drop table test_238 cascade;
