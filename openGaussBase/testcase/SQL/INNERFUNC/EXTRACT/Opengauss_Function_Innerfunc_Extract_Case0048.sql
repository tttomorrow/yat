-- @testpoint: extract(field from timestamp)从给定的时间戳里获取它是一年的第几天的值
--（field的取值范围：doy一年的第几天（1~365/366））
select extract(doy from timestamp '2001-02-16 20:38:40') from sys_dummy;