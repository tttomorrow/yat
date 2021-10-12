--  @testpoint:创建函数，指定参数ROWS，估计函数返回的行数是-1，合理报错
drop FUNCTION if EXISTS compute3;
CREATE  FUNCTION compute3(i int, out result_1 bigint, out result_2 bigint)
returns SETOF RECORD
as $$
begin
    result_1 = i + 1;
    result_2 = i * 10;
return next;
end;
$$language plpgsql
ROWS -1;
/