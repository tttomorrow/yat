-- @testpoint: 类型转换函数to_number将字符串类型的值转换为指定格式的数字，入参为有效值


select to_number('12,454.8-', '99g999d9s');

-- 模式串9长度超过数字个数
select to_number('12,454,234-', '9999999g999g999d9s');

-- 模式串9长度比数字个数短，四舍五入
select to_char('12345.6789','999999d99');

-- 转换16进制到十进制
select to_number('5f','xxx');

-- 模式串0长度比数字个数长，正常显示
select to_number('89.988','00000d00000');

-- 模式串0长度比数字个数短，截取显示
select to_number('89.988888','999d00');
select to_number('98877788','0000');

