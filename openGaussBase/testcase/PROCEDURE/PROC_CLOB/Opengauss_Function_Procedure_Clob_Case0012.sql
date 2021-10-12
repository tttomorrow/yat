-- @testpoint: 存储过程clob数据类型的测试，clob和char/varchar类型的转换结合%type类型

drop table if exists proc_clob_table_012;
create table proc_clob_table_012(t1 int,t2 char(8000),t3 varchar2(8000));

--创建存储过程
create or replace procedure proc_clob_012() is
v1 proc_clob_table_012.t2%type;
v2 proc_clob_table_012.t3%type;
begin
    select t2 into v1 from proc_clob_table_012 where t1=1;
    select t3 into v2 from proc_clob_table_012 where t1=1;
    raise info 'result:%',rtrim(v1);
    raise info'result:%',v2;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_clob_012();

--修改列属性
--增加临时列
alter table proc_clob_table_012 add t4 clob;
alter table proc_clob_table_012 add t5 clob;
--把数据放到临时列，置空数据列
update proc_clob_table_012 set t4=t2 ,t2=null;
update proc_clob_table_012 set t5=t3 ,t3=null;
--修改字段类型
alter table proc_clob_table_012 modify t2 clob;
alter table proc_clob_table_012 modify t3 clob;
--放回数据
update proc_clob_table_012 set t2=t4,t3=t5 where t4 is not null;
--删除临时列
alter table proc_clob_table_012 drop column t4;
alter table proc_clob_table_012 drop column t5;

--再编译存储过程
create or replace procedure proc_clob_012() is
v1 proc_clob_table_012.t2%type;
v2 proc_clob_table_012.t3%type;
begin
    select t2 into v1 from proc_clob_table_012 where t1=1;
    select t3 into v2 from proc_clob_table_012 where t1=1;
    raise info 'result:%',rtrim(v1);
    raise info'result:%',v2;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_clob_012();

--恢复环境
drop procedure if exists proc_clob_012;
drop table if exists proc_clob_table_012;