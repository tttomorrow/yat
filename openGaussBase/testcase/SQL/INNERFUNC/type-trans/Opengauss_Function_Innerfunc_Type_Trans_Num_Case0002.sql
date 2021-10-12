-- @testpoint: 类型转换函数to_number，将字符串类型的值转换为指定格式的数字，入参为无效值时合理报错


-- 非数字类型 + 模式串
SELECT to_number('openguass', '99G999D9S');

-- 其它类型 + 模式串
SELECT to_number('0b101010', '99G999D9S');

-- 数字 + 错误格式
SELECT to_number('233', '8675645');

-- 非数字 + 错误格式
SELECT to_number('高斯', 'xxx');

-- 多参
SELECT to_number('12,454.8-', '99G999D9S','999');

-- 少参
SELECT to_number( , '99G999D9S');

-- 空值
SELECT to_number(' ', '99G999D9S');

-- 特殊字符
SELECT to_number('1……&（*%……', '……&*%……&');