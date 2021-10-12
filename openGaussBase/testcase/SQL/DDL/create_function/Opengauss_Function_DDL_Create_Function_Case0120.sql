--  @testpoint:创建函数，函数未返回集时，使用rows参数，合理报错
drop FUNCTION if EXISTS compute4;
CREATE  FUNCTION compute4(i int, out result_1 bigint, out result_2 bigint)
returns  int
as $$
begin
    result_1 = i + 1;
    result_2 = i * 10;
return next;
end;
$$language plpgsql
ROWS 100;
/