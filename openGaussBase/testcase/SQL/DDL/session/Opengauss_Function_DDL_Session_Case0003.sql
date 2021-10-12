-- @testpoint: 设置所属的模式
drop schema if exists dm;
CREATE SCHEMA dm;
ALTER SESSION SET CURRENT_SCHEMA TO dm;
ALTER SESSION SET CURRENT_SCHEMA TO public;
drop schema dm;