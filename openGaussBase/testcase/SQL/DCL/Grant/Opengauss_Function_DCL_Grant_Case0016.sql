
-- @testpoint: 回收权限


drop user if exists manager cascade;
CREATE ROLE manager PASSWORD 'Bigdata@123';
drop user if exists user_016;
CREATE USER user_016 PASSWORD 'Bigdata@123';
GRANT ALL PRIVILEGES TO user_016;
GRANT user_016 TO manager WITH ADMIN OPTION;
REVOKE ADMIN OPTION FOR user_016 FROM manager CASCADE;
drop user  user_016;
drop user  manager;