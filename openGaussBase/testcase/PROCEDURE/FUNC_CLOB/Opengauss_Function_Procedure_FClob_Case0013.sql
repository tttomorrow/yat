-- @testpoint: 测试clob类型作为自定义函数的参数,和字符串处理函数upper结合

drop table if exists fvt_func_clob_table_013;
create table fvt_func_clob_table_013(
  t1 int,
  t2 clob
  );

--创建自定义函数
create or replace function fvt_func_clob_013(p1 clob) return clob
is
p2 clob;
begin
  p2 := upper(p1);
  insert into fvt_func_clob_table_013 values(1,p2);
  return p2;
  exception
  when no_data_found
  then
    raise info 'no_data_found';
end;
/
--调用自定义函数
select  fvt_func_clob_013('asfghaagghh字符串1123454%……&009#￥');
select * from fvt_func_clob_table_013;

--恢复环境
drop table if exists fvt_func_clob_table_013;
drop function if exists fvt_func_clob_013;
