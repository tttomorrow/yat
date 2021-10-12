-- @testpoint: 类型转换函数to_char (datetime/interval [, fmt])datetime或者interval值按照fmt指定的格式转换为varchar类型，日期为数字加英文单词时合理报错

-- date
select to_char(date 'epoch', 'hh12:mi:ss yyyy-month-dd');
select to_char(time 'allballs', 'hh12:mi:ss ms');

-- timestamp
select to_char(timestamp '2000-12-05 00:00:00', 'mon-dd-yyyy');
select to_char(timestamp 'tomorrow', 'hh12:mi:ss');
select to_char(timestamp 'yesterday', 'hh24:mi:ss');

-- timestamp with time zone
select to_char(timestamp with time zone '2010-09-13 12:32:03+08', 'hh12:mi:ss');
select to_char(timestamp with time zone '2015-10-14 11:21:28.317367 pst', 'hh12:mi:ss');
select to_char(timestamp with time zone '2015-10-14 11:21:28.317367 america/new_york', 'hh12:mi:ss');
select to_char(timestamp with time zone '2015-10-14 11:21:28.317367+08', 'hh12:mi:ss');

-- timestamp without time zone
select to_char(timestamp without time zone '2010-09-13 12:32:03+08');

-- interval
select to_char(interval '1-2', 'y mm');
select to_char(interval '1-1', 'ddd');
select to_char(interval '3 14:05:06', 'ddd hh12:mi:ss');
select to_char(interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds', 'yyyy-mon-dd hh24:mi:ss');
select to_char(interval 'p1y2m3dt4h5m6s', 'ddd hh24:mi:ss');
select to_char(interval 'p0001-02-03t04:05:06', 'ddd hh24:mi:ss');
