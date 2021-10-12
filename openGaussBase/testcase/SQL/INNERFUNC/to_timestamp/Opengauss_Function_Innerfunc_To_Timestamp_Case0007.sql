-- @testpoint: 类型转换函数to_timestamp，入参为非法日期时合理报错

select to_timestamp('0000-05-12','yyyy-mm-dd');
select to_timestamp('2018-00-12','yyyy-mm-dd');
select to_timestamp('2018-09-00','yyyy-mm-dd');
select to_timestamp('2018-09-31','yyyy-mm-dd');