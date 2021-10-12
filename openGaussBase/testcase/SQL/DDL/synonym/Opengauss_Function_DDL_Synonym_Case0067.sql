-- @testpoint: 创建建存储过程的同义词，修改同义词属主（属主为存在+不存在+存在无create权限）,不存在+存在无create权限,合理报错
--建存储过程
drop procedure if exists SYN_PEOC_001;
create or replace procedure SYN_PEOC_001()
as
begin
    raise info '%','test call+synonym';
end;
/
--建同义词
drop SYNONYM if exists SYN_PROC_SYN_001;
create SYNONYM SYN_PROC_SYN_001 for SYN_PEOC_001;
--创建用户
drop user if exists syn004_test004;
create user syn004_test004 password 'Test@123';
--修改为存在的属主：新属主无create权限：报错
alter synonym SYN_PROC_SYN_001 owner to syn004_test004;
--修改为不存在的属主：报错
drop user if exists test05_syn05;
alter synonym SYN_PROC_SYN_001 owner to test05_syn05;
--修改为存在的属主：新属主有create权限
GRANT ALL PRIVILEGES TO syn004_test004;
alter synonym SYN_PROC_SYN_001 owner to syn004_test004;
--清理数据
drop user if exists syn004_test004 cascade;
drop procedure if exists syn_proc_001;
drop synonym if exists SYN_PROC_SYN_001 cascade;
drop procedure if exists SYN_PEOC_001;