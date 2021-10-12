-- @testpoint: 关键字valid,设置指定账号的有效期

--指定用户有效期的起止时间
drop user if exists valid_test_01;
create user valid_test_01 with login password 'gauss@123' valid begin '2010-01-01' valid until '2030-12-31';

--指定用户有效期的开始时间
drop user if exists valid_test_02;
create user valid_test_02 with login password 'gauss+123' valid begin '2010-01-01';

--指定用户有效期的结束时间
drop user if exists valid_test_03;
create user valid_test_03 with login password 'gauss#123' valid until '2050-05-05';

--修改用户有效期的起止时间
alter user valid_test_01 with valid begin '2020-01-01' valid until '2030-12-31';
drop user if exists valid_test_01;
drop user if exists valid_test_02;
drop user if exists valid_test_03;

