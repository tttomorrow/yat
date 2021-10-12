-- @testpoint: 不支持在事务、函数和存储过程中使用 合理报错

--创建序列
drop sequence if exists test_seq_012;
CREATE sequence test_seq_012;
--查询cache值
select last_value,cache_value from test_seq_012;

--不支持在事务、函数和存储过程中使用
begin
    alter sequence test_seq_012 cache 5;
end;
/
select last_value,cache_value from test_seq_012;
select nextval('test_seq_012');
--不支持在函数中使用
create or replace function fun_seq_012() return int
as
begin
    alter sequence test_seq_012 cache 10;
	return 1;
end;
/
select fun_seq_012();
select last_value,cache_value from test_seq_012;
select nextval('test_seq_012');
--不支持在存储过程中使用
create or replace procedure pro_seq_012() is
v1 blob;
begin
    alter sequence test_seq_012 cache 15;
end;
/
call pro_seq_012();
select last_value,cache_value from test_seq_012;
select nextval('test_seq_012');
--查询cache值

select nextval('test_seq_012');
alter sequence test_seq_012 maxvalue 40;
select last_value,cache_value,max_value from test_seq_012;
select nextval('test_seq_012');

--清理环境
drop sequence if exists test_seq_012;
drop procedure if exists fun_seq_012;
drop procedure if exists pro_seq_012;