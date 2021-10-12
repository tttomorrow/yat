-- @testpoint: ALTER SYSTEM SET方法设置lc_messages参数，合理报错
--查询默认
show lc_messages;
--设置，报错
ALTER SYSTEM SET lc_messages to 'C';
--no need to clean