-- @testpoint: 类型转换函数to_char(interval, text)时间间隔类型的值转换为指定格式的字符串，入参为无效值时合理报错

select to_char(interval'1月2日','month dy');
select to_char(interval '15h-2m$12s', 'hh32:mi:ss');
select to_char(interval '2' year ,'yyyy','yyyy');
select to_char(interval '&**&%' ,'yyyy');
select to_char(interval 2 year);
