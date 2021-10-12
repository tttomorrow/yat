-- @testpoint: 查看server_encoding,报告当前数据库的服务端编码字符集

--通过show方式查看
show server_encoding;

--通过系统视图pg_settings查看
select setting from pg_settings where name='server_encoding';