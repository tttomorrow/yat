-- @testpoint: 验证cast函数是否能将整型数据转换为日期数据，合理报错
-- @modify at: 2020-11-16
drop table if exists TEST_CAST;   
create table TEST_CAST as select CAST(990108 AS date) AS birthday;
select * from TEST_CAST;
drop table if exists TEST_CAST;  