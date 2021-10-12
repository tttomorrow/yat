-- @testpoint: 关键字xml，用作函数名


drop function if exists xml(num1 bigint,num2 bigint);
create function xml(num1 bigint,num2 bigint)
return bigint
as
begin
    return num1+num2;
end;
/

select * from xml(55555,666666);
drop function if exists xml(num1 bigint,num2 bigint);