-- @testpoint: 类型转换函数to_timestamp，入参有中文时合理报错

select to_timestamp('2018-01-15','年月日');
select to_timestamp('时间','yyyy');