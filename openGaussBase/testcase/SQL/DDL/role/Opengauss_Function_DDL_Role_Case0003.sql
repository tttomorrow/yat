-- @testpoint: 创建角色并设置其生效时间和失效时间
drop ROLE if exists miriam;
CREATE ROLE miriam WITH LOGIN PASSWORD 'Bigdata@123' VALID BEGIN '2015-01-01' VALID UNTIL '2026-01-01';
drop ROLE if exists miriam;

