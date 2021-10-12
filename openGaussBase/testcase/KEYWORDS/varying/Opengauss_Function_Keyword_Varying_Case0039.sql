-- @testpoint: 关键字varying,用作函数名

drop function if exists varying;
create function varying(num1 int,num2 int)
return int
as
begin
    return num1+num2;
end;
/

select * from varying(555,555);
drop function if exists varying;
