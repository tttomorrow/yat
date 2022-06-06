-- @testpoint: select语句绑定blob类型的参数

--创建存储过程
create or replace procedure pro_017()
as
    sqlstat varchar(500);
	v1 blob;
	r1 blob;
begin
    v1 := '10101111111111';
    sqlstat := 'select :p1';
    execute immediate sqlstat into r1 using v1;
    raise info 'result:%',v1;
end;
/
--调用存储过程
call pro_017();

--清理环境
drop procedure pro_017;