--  @testpoint:创建函数，指定参数ROWS，估计函数返回的行数是null，合理报错
drop FUNCTION if EXISTS compute2;
CREATE  FUNCTION compute2(i int, out result_1 bigint, out result_2 bigint)
returns SETOF RECORD
as $$
begin
    result_1 = i + 1;
    result_2 = i * 10;
return next;
end;
$$language plpgsql
ROWS null;
/