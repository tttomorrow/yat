--  @testpoint:关键字xmlforest，用作函数名(合理报错)


create function xmlforest(num1 integer,num2 integer)
return integer
as
begin
    return num1+num2;
end;
/

select * from xmlforest(5,8);