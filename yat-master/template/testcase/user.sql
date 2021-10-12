create user test_001 identified by 'gauss_123';
grant create session, create procedure, create trigger to test_001;
drop user test_001;
