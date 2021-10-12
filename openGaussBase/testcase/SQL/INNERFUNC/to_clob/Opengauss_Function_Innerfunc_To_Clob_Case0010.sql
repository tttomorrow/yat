-- @testpoint: 创建函数，将varchar类型，转换为clob类型
create or replace function  f_to_clob(in_char varchar) return clob
is
p1 varchar:='nihao';
begin
  return to_clob(p1);
end;
/

select f_to_clob('111');
drop function f_to_clob;
