-- @testpoint: select语句绑定数值类型

--创建存储过程
create or replace procedure pro_006()
as
    sqlstat varchar(500);
	v1 integer;
	v2 bigint;
	v3 real;
	v4 decimal;
	v5 number;
	v6 smallint;
	r1 integer;
	r2 bigint;
	r3 real;
	r4 decimal;
	r5 number;
	r6 smallint;
begin
	v3 := 1.7e;
	v4 := 1.0e127;
	v5 := 1.0e127;
	v6 := 12345;
    sqlstat := 'select :p1,:p2,:p3,:p4,:p5,:p6';
    execute immediate sqlstat into r1,r2,r3,r4,r5,r6 using v1,v2,v3,v4,v5,v6;
    raise info 'result:%',v1;raise info 'result:%',v2;raise info 'result:%',v3;raise info 'result:%',v4;raise info 'result:%',v5;raise info 'result:%',v6;
end;
/
--调用存储过程
call pro_006();

--清理环境
drop procedure pro_006;