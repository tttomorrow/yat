-- @testpoint: select语句绑定布尔类型

--创建存储过程
create or replace procedure pro_005()
as
    sqlstat varchar(500);
	v1 boolean;
	v2 boolean;
	v3 boolean;
	r1 boolean;
	r2 boolean;
	r3 boolean;
begin
    v1 := true;
    v2 := false;
    v3 := 10;
    sqlstat := 'select :p1,:p2,:p3';
    execute immediate sqlstat into r1,r2,r3 using v1,v2,v3;
    raise info 'result:%',r1;
    raise info 'result:%',r2;
    raise info 'result:%',r3;
end;
/
--调用存储过程
call pro_005();

--清理环境
drop procedure pro_005;