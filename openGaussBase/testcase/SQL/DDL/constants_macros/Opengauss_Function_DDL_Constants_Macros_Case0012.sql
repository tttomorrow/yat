-- @testpoint: SESSION_USER无效性测试,合理报错
--session_user(),合理报错
select session_user();
--session_users,合理报错
select session_users;