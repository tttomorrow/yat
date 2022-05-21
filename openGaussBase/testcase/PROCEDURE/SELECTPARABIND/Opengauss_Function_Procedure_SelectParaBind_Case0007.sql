-- @testpoint: select语句绑定字符串类型

--创建存储过程
create or replace procedure pro_007()
as
    sqlstat varchar(500);
	v1 char(15);
	v2 varchar(4000);
	v3 varchar2(4000);
	r1 char(15);
	r2 varchar(4000);
	r3 varchar2(4000);
begin
    v1 := '2147483647';
	v2 := '9223372036854775807';
	v3 := 1e+308;
    sqlstat := 'select :p1,:p2,:p3';
    execute immediate sqlstat into r1,r2,r3 using v1,v2,v3;
raise info 'result:%',v1;
raise info 'result:%',v2;
raise info 'result:%',v3;
end;
/
--调用存储过程
call pro_007();

--清理环境
drop procedure pro_007;
