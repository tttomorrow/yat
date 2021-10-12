-- @testpoint: 创建存储过程时使用current_user，合理报错

create or replace procedure pro(p1 integer) current_user
is
c1 varchar(10);
begin
    c1 := 'gauss';
    raise info '-%',c1;
    raise info ':%',p1;
end;
/
drop procedure if exists pro;
