-- @testpoint: 类型转换函数to_timestamp，入参为非法格式，合理报错

select to_timestamp('2018-01-15','yyyy');
select to_timestamp('2018-01-15','yyyy-mm');
select to_timestamp('09-18 06:25:46','yyyy-mm-dd HH:MI:SS:FF');
select to_timestamp('2018-09 16:25:46:45354','yyyy-mm-dd hh24:mi:ss:ff');