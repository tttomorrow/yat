-- @testpoint: 类型转换函数rawtohex(string)，将一个二进制构成的字符串转换为十六进制的字符串，入参为无效值时合理报错

--x被当作非a-f
SELECT hextoraw('0X8');
SELECT hextoraw(0x8);

--f以外字符
SELECT hextoraw('abcdefg');
SELECT hextoraw('5K');

--多参、少参、空值
SELECT hextoraw();
SELECT hextoraw(' ');
SELECT hextoraw('6D','999');

--特殊字符
SELECT hextoraw('@#$');

-- 浮点数
SELECT hextoraw('5.4');