-- @testpoint: 类型转换函数to_timestamp，入参为正常格式

select to_timestamp('05 dec 2020', 'dd mon yyyy');
select to_timestamp('12-sep-2024');
select to_timestamp('98','rr');
select to_timestamp('2018-09','yyyy-mm');
select to_timestamp('2018-01-15','yyyy-mm-dd');
select to_timestamp('2018-09-18 06:25:46','yyyy-mm-dd hh:mi:ss:ff');
select to_timestamp('2018-09-18 16:25:46:45354','yyyy-mm-dd hh24:mi:ss:ff');