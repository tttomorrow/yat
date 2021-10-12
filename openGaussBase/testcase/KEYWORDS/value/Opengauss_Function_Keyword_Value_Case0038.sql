-- @testpoint: 关键字value,用作函数名

drop function if exists value;
create function value(num1 int,num2 int)
return int
as
begin
    return num1+num2;
end;
/

select * from value(555,555);
drop function if exists value;
