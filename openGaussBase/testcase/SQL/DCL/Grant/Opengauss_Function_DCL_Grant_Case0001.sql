
-- @testpoint:  将系统权限授权给用户或者角色。
--（系统权限又称为用户属性，包括SYSADMIN、CREATEDB、CREATEROLE、AUDITADMIN和LOGIN。）

drop user if exists user_001 cascade;
create user  user_001 identified by 'Gauss_234';

GRANT ALL  PRIVILEGES  TO user_001;
REVOKE ALL PRIVILEGES from user_001;
drop user  user_001;
