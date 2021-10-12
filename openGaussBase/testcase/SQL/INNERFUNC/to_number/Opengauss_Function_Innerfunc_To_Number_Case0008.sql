-- @testpoint: 类型转换函数to_number，参数为非数字,合理报错

select to_number('你好', '99G999D9S');
select to_number('@#$', '99G999D9S');