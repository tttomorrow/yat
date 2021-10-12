-- @testpoint: 具有异常处理的存储过程中进行事务管理

drop table if exists test1;
create table test1 (a int);

--创建存储过程
create or replace procedure transaction_test3()
as
begin
	insert into test1 (a) values (1);
    commit;
    insert into test1 (a) values (1/0);
    commit;
exception
    when division_by_zero then
	raise notice 'caught division_by_zero';
end;
/
--调用存储过程
call transaction_test3();
--清理环境
drop table if exists test1;
drop procedure transaction_test3;