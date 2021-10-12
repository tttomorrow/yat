-- @testpoint: 类型转换函数to_char (datetime/interval [, fmt])，入参为无效参数时合理报错

-- date
select to_char('epoch', 'hh12:mi:ss yyyy-month-dd');
select to_char(epoch, 'hh12:mi:ss yyyy-month-dd');
select to_char(date 'allballs', 'hh24:mi:ss ms');

-- timestamp
select to_char(timestamp 'yesterdayq', 'mi:ss');

-- timestamp with time zone
select to_char(timestamp with time zone '2015-10-14 11:21:28.317367 america/new_yorkkk', 'hh12:mi:ss');

-- interval
select to_char(interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds', 'yyyy-mon-dd hh24:mi:ss');
select to_char(interval '-14:05:06', 'ss');

-- 不加关键字
select to_char('2020-08-26 14:57:33','yyyy-mon-dd hh24:mi:ss');

-- 错格式
select to_char(current_timestamp, 0x5d);
select to_char(pg_systimestamp(), #%&^);

-- 时间戳错误
select to_char(timestamp '2020-08-2614:57:33.23813+08','hh12:mi:ss.ms yy-month-dd');
select to_char(timestamp '2020-08-26 14，57，33.23813+08','hh12:mi:ss yy-month-dd');
