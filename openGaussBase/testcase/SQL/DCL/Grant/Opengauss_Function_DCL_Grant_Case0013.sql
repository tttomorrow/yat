-- @testpoint: 将过程语言的访问权限赋予给指定的用户或角色

drop user if exists user_013 cascade;
create user user_013 identified by 'Gauss_234';

grant usage on language sql to user_013;

revoke all privileges on language sql from user_013;

drop user if exists user_013;