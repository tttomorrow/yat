-- @testpoint: 变量定义成current_user

create or replace procedure pro(p1 integer) authid current_user
is
current_user varchar(10);
begin
    current_user := 'gauss';
    raise info '-%',current_user;
    raise info ':%',p1;
end;
/
--调用存储过程
call pro(10);

--清理环境
drop procedure if exists pro;
