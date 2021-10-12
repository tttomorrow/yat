-- @testpoint: 关键字volatile,用作函数名

drop function if exists volatile;
create function volatile(num1 int,num2 int)
return int
as
begin
    return num1+num2;
end;
/

select * from volatile(123,456);
drop function if exists volatile;