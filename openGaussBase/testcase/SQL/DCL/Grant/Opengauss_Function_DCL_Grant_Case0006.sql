-- @testpoint: 可以给用户授权->CREATE TABLE

drop user if exists user_001 cascade;
create user  user_001 identified by 'Gauss_234';
drop table if exists t1;
create table t1(id int ,name char(255),age int ,city varchar (255));
GRANT ALL  ON t1 TO user_001;
--回收权限

REVOKE  ALL PRIVILEGES ON  TABLE t1 FROM user_001;
drop table if exists t1;
drop user  user_001;