-- @testpoint: 类型转换函数to_timestamp，入参为表达式时合理报错

select to_timestamp('2018-01-15',3>2);
select to_timestamp('2018>2017','yyyy');