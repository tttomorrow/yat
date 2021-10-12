--  @testpoint:关键字xmlattributes，用作函数名(合理报错)


create function xmlattributes(num1 bigint,num2 bigint)
return bigint
as
begin
    return num1+num2;
end;
/

select * from xmlattributes(55555,666666);

