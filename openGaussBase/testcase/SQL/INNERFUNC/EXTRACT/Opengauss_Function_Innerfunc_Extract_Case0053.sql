-- @testpoint: extract(field from timestamp)从给定的时间戳里获取秒域的值
--（field的取值范围：microseconds秒域（包括小数部分）乘以1,000,000）
select extract(microseconds from time '17:12:28.5') from sys_dummy;