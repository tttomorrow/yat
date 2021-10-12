-- @testpoint: 关键字within，用作函数名


drop function if exists within;
create function within(num1 integer,num2 integer)
return integer
as
begin
    return num1+num2;
end;
/

select * from within(56,78);
drop function if exists within;