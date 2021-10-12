-- @testpoint: ALTER SYSTEM SET方法设置参数statement_timeout，合理报错
ALTER SYSTEM SET statement_timeout to 10;
--no need to clean