-- @testpoint: to_timestamp(text, text)字符串类型的值转换为指定格式的时间戳，入参为有效值

select to_timestamp('01','rr');
select to_timestamp('98','rr');
select to_timestamp('-1','syyyy');
select to_timestamp('12-sep-10 14:10:10.123000','dd-mon-yyy hh24:mi:ss.ff');
select to_timestamp('12-september-10 14:10:10.123000','dd-month-yy hh24:mi:ss.ff pm');
select to_timestamp('12-sep-14','dd-mon-yy');
select to_timestamp('120 2014','ddd yyyy');
select to_timestamp('sep-14','mon-yy');
select to_timestamp('05 dec 2000', 'dd mon yyyy');
