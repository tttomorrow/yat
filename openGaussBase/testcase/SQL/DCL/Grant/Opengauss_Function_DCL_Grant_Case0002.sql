-- @testpoint:将对象权限授权给用户或者角色

drop user if exists user_001 cascade;
create user  user_001 identified by 'Gauss_234';

drop table if exists t1;
create table t1(id int ,name char(255),age int ,city varchar (255));

GRANT select (id,name,age),update (city) ON t1 TO user_001;

--回收指定表的select 权限

REVOKE  GRANT OPTION FOR
SELECT ON  TABLE t1
FROM user_001;



drop table if exists t1;
drop user  user_001;
