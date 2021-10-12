-- @testpoint: extract(field from timestamp)从给定的时间戳里获取该天所在的该年的季度的值
--（field的取值范围：quarter该天所在的该年的季度（1-4））
select extract(quarter from timestamp '2001-02-16 20:38:40') from sys_dummy;