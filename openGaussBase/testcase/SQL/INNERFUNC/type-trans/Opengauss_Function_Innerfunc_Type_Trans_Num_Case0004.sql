-- @testpoint: 类型转换函数to_number，将字符串类型的值转换为指定格式的数字，入参为无效值时合理报错


-- 十六进制转十进制，原始超过16个字节
select to_number('123456781234567812345678123456781234567812345678123456781234567812345678123456781234567812345678123456781234567812345678123456789','xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');

-- 十六进制转十进制，模式串有除了x/x以外的字符
select to_number('5f','xjx');

-- 非字符类型 + 模式串
select to_number('0b11', '99g999d9s');

-- 其它类型 + 模式串
select to_number('0b101010', '99g999d9s');

-- 字符 + 错误格式
select to_number('233', '8675645');

-- 非数字字符 + 错误格式
select to_number('高斯', 'xxx');

-- 多参
select to_number('12,454.8-', '99g999d9s','999');

-- 少参
select to_number( , '99g999d9s');

-- 空值
select to_number(' ', '99g999d9s');

-- 特殊字符
select to_number(<1*8+9/3-9%3+9/2>, '999999d99');