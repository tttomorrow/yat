-- @testpoint: 存储过程clob数据类型的测试，测试clob类型作为存储过程的参数,和字符串处理函数upper结合


drop table if exists proc_clob_table_013;
create table proc_clob_table_013(t1 int,t2 clob);

--创建存储过程
create or replace procedure proc_clob_013(p1 in clob,p2 out clob) is
begin
    p2 := upper(p1);
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/

--调用存储过程
declare
v1 text :='asfghaagghh字符串1123454%……&009#￥';
v2 clob;
begin
  proc_clob_013(v1,v2);
  insert into proc_clob_table_013 values(1,v2);
end;
/

select * from proc_clob_table_013;

--恢复环境
drop table proc_clob_table_013;
drop procedure proc_clob_013;
