--  @testpoint:关键字xmlelement，用作函数名(合理报错)


create function xmlelement(num1 varchar(10),num2 varchar(20))
return varchar
as
begin
    return num1||num2;
end;
/

select * from xmlelement('hello','openGauss');

