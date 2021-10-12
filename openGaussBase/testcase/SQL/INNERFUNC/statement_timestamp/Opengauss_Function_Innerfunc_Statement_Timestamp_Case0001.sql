-- @testpoint: 给的错误参数，合理报错
-- @description: statement_timestamp(),获取当前日期及时间


select statement_timestamp from sys_dummy;
select statement_timestamp('') from sys_dummy;
select statement_timestamp(' ') from sys_dummy;
select statement_timestamp(null) from sys_dummy;
select statement_timestamp('2017-09-01 17:04:39') from sys_dummy;
select statement_timestamp('2017-09-01 17:04:39.119267+08') from sys_dummy;