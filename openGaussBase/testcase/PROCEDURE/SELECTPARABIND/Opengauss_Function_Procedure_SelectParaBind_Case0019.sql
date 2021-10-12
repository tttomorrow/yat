-- @testpoint: 绑定参数的个数与using个数不一致，合理报错

--创建存储过程
create or replace procedure pro_019()
as
    sqlstat varchar(500);
	v1 date;
	v2 timestamp;
	r1 date;
	r2 timestamp;
begin
    v1 := to_date('2020-11-24 13:14:15', 'yyyy-mm-dd hh24:mi:ss');
	v2 := to_date('2020-11-24 13:14:15', 'yyyy-mm-dd hh24:mi:ss');
    sqlstat := 'select :p1,:p2,:p3,:p4,:p5';
    execute immediate sqlstat into r1,r2 using v1,v2;
    raise info 'result:%',v1;
    raise info 'result:%',v2;
end;
/
--调用存储过程
call pro_019();

--清理环境
drop procedure pro_019;

