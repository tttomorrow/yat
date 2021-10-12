-- @testpoint: 验证cast函数是否能将整型数据转换为日期时间型，合理报错
-- @modify at: 2020-11-16
 drop table if exists TEST_CAST;   
 create table TEST_CAST as select CAST(19890616 AS timestamp) AS birthday;
 drop table if exists TEST_CAST;