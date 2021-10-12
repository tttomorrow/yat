-- @testpoint: 类型转换函数to_char(timestamp, text)时间戳类型的值转换为指定格式的字符串，入参为有效值

-- 实时的值
-- select to_char(current_timestamp, 'hh12:mi:ss');
-- select to_char(pg_systimestamp(), 'hh12:mi:ss');
-- select to_char(pg_systimestamp(), 'yyyy-mon-dd   hh24:mi:ss ');

-- 给定时间戳
select to_char(timestamp '2020-08-26 14:57:33.23813+08','hh12:mi:ss.ms yy-month-dd');
select to_char(timestamp '2020-08-26 14:57:33.23813+08','hh12:mi:ss yy-month-dd');
select to_char(timestamp '2020-08-26 14:57:33.23813+08','yyy-mon-dd ^&* hh12:mi:ss');
