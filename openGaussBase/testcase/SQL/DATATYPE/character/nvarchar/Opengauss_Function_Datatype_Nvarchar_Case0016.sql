-- @testpoint: 存储过程和函数调用和返回nvarchar

--step1:创建函数返回和调用nvarchar; expect:成功
create or replace function fun_nvarchar_0016 (c_nvarchar nvarchar) return nvarchar
as
b nvarchar(1024);
begin
    b:=c_nvarchar||c_nvarchar;
    return b;
end;
/

select fun_nvarchar_0016('test0016'::nvarchar);

--step2:创建存储过程调用nvarchar; expect:成功
create or replace procedure proc_nvarchar_0016(c_nvarchar nvarchar)
as
b nvarchar(8000);
begin
    b:=c_nvarchar||c_nvarchar;
    raise info '%',b;
end;
/
select proc_nvarchar_0016('test0016');

--step3:清理环境; expect:成功
drop function fun_nvarchar_0016(nvarchar);
drop function proc_nvarchar_0016(nvarchar);