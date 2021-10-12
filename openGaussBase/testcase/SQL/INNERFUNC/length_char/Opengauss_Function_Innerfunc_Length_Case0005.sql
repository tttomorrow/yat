-- @testpoint: 字符处理函数length空值测试
select length('') from sys_dummy;
select length(null) from sys_dummy;