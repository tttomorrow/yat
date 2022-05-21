-- @testpoint: 类型转换函数to_date(text)将文本类型的值转换为指定格式的时间戳，入参为无效值时合理报错

select to_date('987417806');
select to_date('2001/0203');
select to_date('#@#$@');
select to_date('二零二零年');
select to_date();
