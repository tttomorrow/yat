-- @testpoint: to_date(text, text)字符串类型的值转换为指定格式的日期，入参为无效值时合理报错

-- 多参少参
select to_date('1999 1 8','YY-MM-DD','999');
select to_date();

-- 不对应
select to_date('1999 1 8','YY-Mon-DD');
select to_date('8-Jan-99', 'DD MONTH YY');
select to_date('二零二零年','YYYY年');
select to_date('1999 13 8','YY-MM-DD');
select to_date('1999 1 98','YY-MM-DD');

-- 特殊月份
select to_date('1999 2 29','YYYY-MM-DD');
select to_date('1999 2 31','YYYY-MM-DD');
