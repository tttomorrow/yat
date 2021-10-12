-- @testpoint: 类型转换函数to_char(interval, text)时间间隔类型的值转换为指定格式的字符串，入参为有效值

select to_char(interval '2' year ,'yyyy');
select to_char(interval '15h 2m 12s', 'hh24:mi:ss');
select to_char(interval '34:05:06','hh12:mi:ss');
select to_char(interval '34:05:06','hh24:mi:ss');
select to_char(interval '3' day ,'ddd');
select to_char(interval '3' day ,'dd');
select to_char(interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds','mi');
select to_char(interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds','yyyy-mm-dd hh:mi:ss');

select to_char(interval '34:05:06','ww');
select to_char(interval '3' day ,'天');
select to_char(interval '1 year 2 months 3 days 4 hours 5 minutes 6 seconds','yyyy&mm*dd hh——mi#ss');
select to_char(interval '2' year ,'dd');


