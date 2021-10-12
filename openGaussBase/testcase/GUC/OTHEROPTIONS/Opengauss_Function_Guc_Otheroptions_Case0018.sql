-- @testpoint: 查看max_identifier_length,报告当前系统允许的标识符最大长度

--通过show方式查看
show max_identifier_length;

--通过系统视图pg_settings查看
select setting from pg_settings where name='max_identifier_length';