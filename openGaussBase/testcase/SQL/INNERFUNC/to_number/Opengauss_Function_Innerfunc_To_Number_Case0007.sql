-- @testpoint: 类型转换函数to_number，参数为非纯数字

select to_number('你好123', '99G999D9S');
select to_number('@123', '99G999D9S');
select to_number('_123', '99G999D9S');
select to_number('$#123', '99G999D9S');