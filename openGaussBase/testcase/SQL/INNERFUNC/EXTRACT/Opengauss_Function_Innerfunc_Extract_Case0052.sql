-- @testpoint: extract(field from timestamp)从给定的时间戳里获取日期中的iso 8601标准年的值
--（field的取值范围：isoyear（不适用于间隔））
select extract(isoyear from date '2006-01-01') from sys_dummy;
select extract(isoyear from date '2006-01-02') from sys_dummy;
