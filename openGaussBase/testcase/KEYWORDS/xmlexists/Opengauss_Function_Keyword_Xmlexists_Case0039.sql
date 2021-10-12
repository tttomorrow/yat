--  @testpoint:关键字xmlexists，用作函数名(合理报错)


create function xmlexists(num1 varchar(10),num2 varchar(20))
return varchar
as
begin
    return num1||num2;
end;
/

select * from xmlexists('hello','openGauss');