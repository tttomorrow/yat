-- @testpoint: 匿名块中进行算数运算

declare
  v_fz number := 3.8e+126;
  v_fm number := 3.8e+127;
begin
  raise notice '%',v_fz / v_fm;
end;
/
