-- @testpoint:  将用户或者角色的权限授权给其他用户或角色。

drop user if exists manager cascade;
CREATE ROLE manager PASSWORD 'Bigdata@123';

CREATE USER user_002 PASSWORD 'Bigdata@123';
GRANT ALL PRIVILEGES TO user_002;
GRANT user_002 TO manager WITH ADMIN OPTION;


drop user  user_002;
drop user  manager;