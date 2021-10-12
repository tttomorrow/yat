-- @testpoint: until,设置用户有效期

drop user if exists until_test;
create user until_test password 'gauss@123' valid until '2050-07-08';

alter user until_test valid until '2030-07-08';

--清理环境
drop user if exists until_test;