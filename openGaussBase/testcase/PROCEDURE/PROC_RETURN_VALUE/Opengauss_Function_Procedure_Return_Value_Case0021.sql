-- @testpoint: 测试存储过程返回值类型——number/decimal,精度溢出的情况 合理报错

--创建存储过程
create or replace procedure proc_return_value_021(p1 decimal)  as
v_dec number(12,6);
begin
    v_dec:=p1;
    raise info 'v_dec=:%',v_dec;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/
--调用存储过程
declare
    v1 number:=999999.999999;
begin
    proc_return_value_021(v1);
end;
/
--调用存储过程,精度溢出
declare
    v2 number:=1999999.999000;
begin
    proc_return_value_021(v2);
end;
/
--清理环境
drop procedure proc_return_value_021;