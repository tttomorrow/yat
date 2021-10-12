-- @testpoint: 类型转换函数to_timestamp，入参多输入/少输入时合理报错

select to_timestamp('2018','yyyy','2018','yyyy');
select to_timestamp('2018-01-15','yyyy-mm','dd');
select to_timestamp('2018-01-15');

