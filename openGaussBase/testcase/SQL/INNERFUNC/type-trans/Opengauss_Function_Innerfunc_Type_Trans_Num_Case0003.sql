-- @testpoint: 类型转换函数to_number ( expr [, fmt])，将expr按指定格式转换为一个number类型的值，入参为有效值

-- 数字转特定格式
select to_number('12,454.8-', '99g999d9s');

-- 十六转十，测x和x
select to_number('5f','xxx');
select to_number('5f','xxxxxxxx');

-- 十六转十进制，边界16个字节
select to_number('1111ffff2222eeee', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');

-- 字符串拼接
select to_number('111+222', '999999g99');

-- 数学表达式
select to_number(111+222, '999999g99');
select to_number(1*8+9/3-9%3+9/2, '999999d99');

