-- @testpoint: 关键字variable,用作函数名

drop function if exists variable;
create function variable(num1 int,num2 int)
return int
as
begin
    return num1+num2;
end;
/

select * from variable(555,555);
drop function if exists variable;
