-- @testpoint: 创建存储过程的同义词，调用同义词，成功
-- @modify at: 2020-11-26
--建存储过程
drop procedure if exists SYN_PEOC_065_001;
create or replace procedure SYN_PEOC_065_001()
as
begin
    raise info '%','test call+synonym';
end;
/
--建同义词
drop SYNONYM if exists SYN_065_001;
create SYNONYM SYN_065_001 for SYN_PEOC_065_001;
--调用
call SYN_065_001();
--清理环境
drop procedure if exists SYN_PEOC_065_001;
drop SYNONYM if exists SYN_065_001;
