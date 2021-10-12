-- @testpoint: 自定义函数clob数据类型的测试--clob和char/varchar类型的转换结合%type类型测试

drop table if exists fvt_func_clob_table_012;
create table fvt_func_clob_table_012(
  t1 int,
  t2 char(8000),
  t3 varchar2(8000)
  );

--创建自定义函数
create or replace function fvt_func_clob_012() return clob
is
v1 fvt_func_clob_table_012.t2%type;
v2 fvt_func_clob_table_012.t3%type;
v3 clob;
begin
  select t2 into v1 from fvt_func_clob_table_012 where t1=1;
  select t3 into v2 from fvt_func_clob_table_012 where t1=1;
  v3:=rtrim(v1)||v2;
  return v3;
  exception
  when no_data_found
  then
    raise info 'no_data_found';
end;
/
--调用自定义函数
select fvt_func_clob_012();

--修改列属性
alter table fvt_func_clob_table_012 add t4 clob;--增加临时列
alter table fvt_func_clob_table_012 add t5 clob;--增加临时列
update fvt_func_clob_table_012 set t4=t2 ,t2=null;
update fvt_func_clob_table_012 set t5=t3 ,t3=null;--把数据放到临时列，置空数据列

alter table fvt_func_clob_table_012 modify t2 clob;--修改字段类型
alter table fvt_func_clob_table_012 modify t3 clob;--修改字段类型
update fvt_func_clob_table_012 set t2=t4,t3=t5 where t4 is not null;--放回数据
alter table fvt_func_clob_table_012 drop column t4;--删除临时列
alter table fvt_func_clob_table_012 drop column t5;--删除临时列

--调用自定义函数
select fvt_func_clob_012();

--恢复环境
drop function if exists fvt_func_clob_012;
drop table if exists fvt_func_clob_table_012;
