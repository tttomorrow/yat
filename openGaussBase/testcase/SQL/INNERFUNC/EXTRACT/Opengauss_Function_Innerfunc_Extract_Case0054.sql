-- @testpoint: extract(field from timestamp)从给定的时间戳里获取千年的值
--（field的取值范围：millennium千年，第三个千年从2001年1月1日零时开始）
select extract(millennium from timestamp '2020-02-16 20:38:40') from sys_dummy;