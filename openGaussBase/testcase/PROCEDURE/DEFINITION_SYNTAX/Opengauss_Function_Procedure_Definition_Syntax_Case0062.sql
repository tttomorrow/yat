-- @testpoint: select into语句中给int数据类型赋值，通过正负转换截取到int类型下边界

declare
  v_int int;
begin
     raise info 'result:% ',v_int;
end;
/