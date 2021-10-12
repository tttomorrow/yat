-- @testpoint: 类型转换函数hextoraw(string)，将一个十六进制构成的字符串转换为二进制，入参为有效值

select hextoraw(5);
select hextoraw('5f');
select hextoraw('6d');
select hextoraw('6');
select hextoraw('0b1010');
select hextoraw('abcdef');
