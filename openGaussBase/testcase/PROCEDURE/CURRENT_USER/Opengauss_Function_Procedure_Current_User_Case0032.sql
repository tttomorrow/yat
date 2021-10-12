-- @testpoint: 在存储过程中创建用户时指定密码并查看

--创建存储过程
create or replace procedure test_proc_using_001()
as
begin
	create user haha identified by "Haha@1234";
end;
/
--调用存储过程
call test_proc_using_001();
select proname,prosrc from pg_proc where proname='test_proc_using_001';

--清理环境
drop procedure test_proc_using_001;
drop user haha;

