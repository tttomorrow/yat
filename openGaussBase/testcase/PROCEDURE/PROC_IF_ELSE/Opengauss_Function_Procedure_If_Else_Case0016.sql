-- @testpoint: 测试存储过程中带有if else的递归调用的if/else语句

--创建存储过程
create or replace procedure PROC_IF_ELSE_016(
n int,
a varchar2,
b varchar2,
c varchar2
) as
v_n int :=n;
v_a char(4) :=a;
v_b char(4) :=b;
v_c char(4) :=c;
v_call_stmt varchar2(128);
begin
    if(1=v_n)
    then   
        raise info '---->%',v_a;
        raise info '---->%',v_c;

    else
		PROC_IF_ELSE_016(v_n-1,v_a,v_c,v_b);
        raise info '---->%',v_a;
        raise info '---->%',v_c;
    end if;
end;
/
--调用存储过程
Call PROC_IF_ELSE_016(4,'qq','ww','ee');

--清理环境
drop procedure PROC_IF_ELSE_016;