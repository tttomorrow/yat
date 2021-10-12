-- @testpoint: 类型转换函数to_timestamp(string [,fmt])，字符串string按fmt指定的格式转换成时间戳类型的值，入参为有效值

show nls_timestamp_format;
select to_timestamp('01','rr');
select to_timestamp('98','rr');
select to_timestamp('-1','syyyy');
select to_timestamp('12-sep-10 14:10:10.123000','dd-mon-yyy hh24:mi:ss.ff');
select to_timestamp('12-september-10 14:10:10.123000','dd-month-yy hh24:mi:ss.ff pm');
select to_timestamp('12-sep-14','dd-mon-yy');
select to_timestamp('120 2014','ddd yyyy');
select to_timestamp('sep-14','mon-yy');
