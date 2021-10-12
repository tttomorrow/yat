-- @testpoint: drop temporary语句删除系统表，合理报错
-- @modify at: 2020-11-24
drop temporary table pg_authid;
drop temporary table pg_class;