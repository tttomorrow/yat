
-- @testpoint:可以给用户授权->CREATE role

drop user if exists user_003 cascade;
create user  user_003 identified by 'Gauss_234';

drop role  if exists  role1 ;
create  role  role1  identified by 'Gauss_234';


--GRANT ALL ON  role1 TO user_003;

grant role1   to user_003;
REVOKE    role1   FROM user_003 ;

drop user if exists user_003 cascade;
drop role  if exists  role1 ;