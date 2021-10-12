-- @testpoint: extract(field from timestamp)从给定的时间戳里获取月份数的值
--（field的取值范围：month）
-- 如果source为timestamp，表示一年里的月份数（1-12）。
select extract(month from timestamp '2001-02-16 20:38:40') from sys_dummy;
-- 如果source为interval，表示月的数目，然后对12取模（0-11）。
select extract(month from interval '2 years 13 months') from sys_dummy;