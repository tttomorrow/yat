-- @testpoint: 类型转换函数to_char(timestamp, text)时间戳类型的值转换为指定格式的字符串，入参为无效值时合理报错

-- 不加关键字
select to_char('2020-08-26 14:57:33','yyyy-mon-dd hh24:mi:ss');

 -- 错格式
select to_char(current_timestamp, 0x5d);
select to_char(pg_systimestamp(), #%&^);

-- 时间戳错误
select to_char(timestamp '2020-08-2614:57:33.23813+08','hh12:mi:ss.ms yy-month-dd');
select to_char(timestamp '2020-08-26 14，57，33.23813+08','hh12:mi:ss yy-month-dd');
