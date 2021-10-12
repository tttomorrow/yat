-- @testpoint: 查看lc_collate,报告当前数据库的字符串排序区域设置

--通过show方式查看
show lc_collate;

--通过系统视图pg_settings查看
select setting from pg_settings where name='lc_collate';