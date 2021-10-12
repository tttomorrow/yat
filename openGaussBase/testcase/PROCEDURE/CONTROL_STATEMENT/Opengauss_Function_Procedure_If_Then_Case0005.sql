-- @testpoint: 条件语句if ...then ...else

create or replace procedure proc_if_else_016(
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
		proc_if_else_016(v_n-1,v_a,v_c,v_b);
        raise info '---->%',v_a;
        raise info '---->%',v_c;
    end if;
end;
/

call proc_if_else_016(4,'qq','ww','ee');

drop procedure proc_if_else_016;