-- @testpoint: 为同一个函数创建n个同义词,使用,再删除
--建表
drop table if exists table_033 cascade;
create table table_033(s varchar);
--插入数据
insert into table_033 values('a'),('b'),('c'),('d');
--创建函数
create or replace function SYN_FUN_001(a number,str varchar) return varchar
as
	cur sys_refcursor;
	var varchar(1024);
	new_var varchar(1024):=str;
begin
	open cur for select str from table_033;
	for i in 1..a loop
		fetch cur into var;
		exit when cur%notfound;
		new_var:=new_var||var;
	end loop;
	return new_var;
end;
/
--存储过程中，创建同义词
create or replace procedure SYN_PROC_00001 (a number)
as
begin
	for i in 1..a loop
		execute immediate 'create or replace synonym SYN_FUN_SYN_00'||i||' for SYN_FUN_001';
	end loop;
end;
/
--调用存储过程
select SYN_PROC_00001(10000);
--存储过程中，使用同义词
create or replace procedure SYN_PROC_00002(a number)
as
str1 varchar(8000);
begin
	for i in 1..a loop
		execute immediate 'select SYN_FUN_SYN_00'||i||'('||i||',null)  from sys_dummy' into str1;
	end loop;
end;
/
select SYN_PROC_00002(10000);
--存储过程中，删除同义词
create or replace procedure SYN_PROC_00003(a number)
as
begin
	for i in 1..a loop
		execute immediate 'drop synonym if exists SYN_FUN_SYN_00'||i;
	end loop;
end;
/
--调用存储过程
select SYN_PROC_00003(10000);
--清理环境
drop function if exists  SYN_FUN_001(a number,str varchar) cascade;
drop procedure if exists  SYN_PROC_00001;
drop procedure if exists  SYN_PROC_00002;
drop procedure if exists  SYN_PROC_00003;
drop table if exists table_033 cascade;
