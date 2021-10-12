-- @testpoint: opengauss关键字password(非保留)，创建角色liming，并设置会话的角色为liming。

CREATE ROLE liming WITH PASSWORD 'Bigdata@123';
ALTER SESSION SET SESSION AUTHORIZATION liming PASSWORD 'Bigdata@123';
ALTER SESSION SET SESSION AUTHORIZATION default;
DROP ROLE liming;


drop schema if exists tpcds CASCADE;
create schema tpcds;
CREATE ROLE tpcds_manager PASSWORD 'Bigdata@123';
GRANT USAGE,CREATE ON SCHEMA tpcds TO tpcds_manager;
REVOKE USAGE,CREATE ON SCHEMA tpcds FROM tpcds_manager;
DROP ROLE tpcds_manager;


create group group_1   password 'Bigdata@123';
drop group group_1;
--清理环境
drop schema if exists tpcds CASCADE;