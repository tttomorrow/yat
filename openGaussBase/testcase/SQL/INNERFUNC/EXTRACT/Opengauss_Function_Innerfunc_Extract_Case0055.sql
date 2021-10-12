-- @testpoint: extract(field from timestamp)从给定的时间戳里获取秒域的值
--（field的取值范围：microseconds秒域milliseconds秒域（包括小数部分）乘以1000。请注意它包括完整的秒）
select extract(milliseconds from time '17:12:28.5') from sys_dummy;