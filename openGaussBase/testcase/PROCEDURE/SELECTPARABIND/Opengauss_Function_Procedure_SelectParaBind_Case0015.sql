-- @testpoint: select语句绑定interval类型

--创建存储过程
create or replace procedure pro_015()
as
    sqlstat varchar(500);
	v1 interval day to second;
	r1 interval day to second;
begin
    v1 := '12 12:3:4.1234';
    sqlstat := 'select :p1';
    execute immediate sqlstat into r1 using v1;
    raise info 'result:%',v1;
end;
/
--调用存储过程
call pro_015();

--清理环境
drop procedure pro_015;