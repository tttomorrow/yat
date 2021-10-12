-- @testpoint: to_timestamp(text, text)字符串类型的值转换为指定格式的时间戳，入参为无效值时合理报错

-- 年份特殊值
select to_timestamp('12-sep-0000', 'dd mon yyyy');
select to_timestamp('12-sep-0', 'dd mon yyyy');
select to_timestamp('12-sep--2014', 'dd mon yyyy');

-- 不匹配  14小时对应hh12
select to_timestamp('12-sep-10 14:10:10.123000','dd-mon-yyy hh12:mi:ss.ff');
select to_timestamp('12-sep-14','ddd-mon-yyy');
select to_timestamp('05 dec 2000', 'dd month yyyy');
select to_timestamp('5009 dec -2000', 'dd mon yyyy');

--修改默认时间戳格式
set nls_timestamp_format to 'dd-month-yy hh:mi:ss.ff am';
select to_timestamp('12-sep-2014');
select to_timestamp('12-september-14');
set nls_timestamp_format to 'dd-mon-yyyy hh:mi:ss.ff am';
select to_timestamp('12-september-14');
select to_timestamp('12-sep-2014');
