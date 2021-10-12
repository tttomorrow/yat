-- @testpoint: sign函数作为自定义函数返回值
drop function if exists test_sign;
create or replace function test_sign(a float) return float
is
begin
return sign(a);
end;
/
select test_sign(99.999);
select test_sign(-99.99);
select test_sign('0');
drop function test_sign;
