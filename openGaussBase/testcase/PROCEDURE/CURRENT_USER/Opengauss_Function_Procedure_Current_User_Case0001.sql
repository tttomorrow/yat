-- @testpoint: 创建存储过程时使用authid current_user

--创建存储过程
create or replace procedure pro(p1 integer) authid current_user
is
c1 varchar(10);
begin
    c1 := 'gauss';
    raise info '-%',c1;
    raise info ':%',p1;
end;
/
--调用存储过程
call pro(10);
--清理环境
drop procedure pro;

--创建存储过程时使用 security invoker
create or replace procedure pro(p1 integer)  called on null input security invoker
is
c1 varchar(10);
begin
     c1 := 'gauss';
    raise info '-%',c1;
    raise info ':%',p1;
end;
/
--调用存储过程
call pro(10);

--清理环境
drop procedure pro;