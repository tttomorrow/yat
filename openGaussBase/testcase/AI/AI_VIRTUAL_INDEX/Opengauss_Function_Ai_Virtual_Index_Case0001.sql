-- @testpoint: 对单表创建虚拟索引,并进行索引查询,删除

--step1:建表1 expect:建表1成功
drop table if exists t_ai_virtual_index_0001_01;
create table t_ai_virtual_index_0001_01(col_int int,col_numeric numeric,
col_float float,col_char char(10),col_text text,col_time time);

--step2:建表2 expect:建表2成功
drop table if exists t_ai_virtual_index_0001_02;
create table t_ai_virtual_index_0001_02(col_int int,col_dec dec,col_money money,col_boolean boolean,col_char char(10),col_clob clob);

--step3:建存储过程 expect:建存储过程成功
create or replace procedure p_virtual_index_0001(a int) is
V_int int;
V_numeric numeric;
V_float float;
V_char char(10);
V_text text;
V_time time;
begin
for i in 1..a
loop
V_int :=i;
V_numeric :=i+1.11;
V_float :=i*5.55;
V_char :='x_'|| i;
V_text :='V_text_'|| i;
V_time :='19:41:20';
execute immediate 'insert into t_ai_virtual_index_0001_01 values
(:p1,:p2,:p3,:p4,:p5,:p6)
'using V_int,V_numeric,V_float,V_char,V_text,V_time;
end loop;
end;
/

--step4:向表1中插入1000000条数据并统计数据的数量 expect:向表1中插入1000000条数据成功,返回表1数据的数量
call p_virtual_index_0001(1000000);
select count(*) from t_ai_virtual_index_0001_01;

--step5:创建虚拟索引1;expect:创建虚拟索引1成功
select * from hypopg_create_index('create index on t_ai_virtual_index_0001_01(col_int)');

--step6:查看执行计划;expect:返回执行计划
explain select t_ai_virtual_index_0001_01.col_int,t_ai_virtual_index_0001_01.col_numeric,t_ai_virtual_index_0001_02.col_money from t_ai_virtual_index_0001_01 left join t_ai_virtual_index_0001_02
on t_ai_virtual_index_0001_01.col_int = t_ai_virtual_index_0001_02.col_int where t_ai_virtual_index_0001_01.col_time='19:41:20' or t_ai_virtual_index_0001_01.col_char in ('x_10000','x_1000000')
order by t_ai_virtual_index_0001_01.col_int desc limit 20;

--step7:删除索引1 expect:删除索引1成功
select * from hypopg_reset_index();

--step8:创建虚拟索引2;expect:创建虚拟索引2成功
select * from hypopg_create_index('create index on t_ai_virtual_index_0001_01(col_int,col_text)');

--step9:查看执行计划;expect:返回执行计划
explain select t_ai_virtual_index_0001_01.col_int,t_ai_virtual_index_0001_01.col_numeric,t_ai_virtual_index_0001_02.col_money from t_ai_virtual_index_0001_01 right join t_ai_virtual_index_0001_02
on t_ai_virtual_index_0001_01.col_int = t_ai_virtual_index_0001_02.col_int where t_ai_virtual_index_0001_01.col_text like 'V_text_2999%' order by t_ai_virtual_index_0001_01.col_int desc limit 20;

--step10:删除索引2 expect:删除索引2成功
select * from hypopg_reset_index();

--step11:创建虚拟索引3 expect:创建虚拟索引3成功
select * from hypopg_create_index ('create index on t_ai_virtual_index_0001_01(col_int)');

--step12:查看执行计划 expect:返回执行计划
explain select t_ai_virtual_index_0001_01.col_int,t_ai_virtual_index_0001_01.col_numeric,t_ai_virtual_index_0001_02.col_money from t_ai_virtual_index_0001_01 left join
t_ai_virtual_index_0001_02 on t_ai_virtual_index_0001_01.col_int = t_ai_virtual_index_0001_02.col_int where t_ai_virtual_index_0001_01.col_time='19:41:20' or t_ai_virtual_index_0001_01.col_char in ('x_10000','x_1000000')
order by t_ai_virtual_index_0001_01.col_int desc limit 20;

--step13:删除索引3 expect:删除索引3成功
select * from hypopg_reset_index();

--step14:创建虚拟索引4 expect:创建虚拟索引4成功
select * from hypopg_create_index ('create index on t_ai_virtual_index_0001_01(col_int,col_text)');

--step15:查看执行计划 expect:返回执行计划
explain select t_ai_virtual_index_0001_01.col_int,t_ai_virtual_index_0001_01.col_numeric,t_ai_virtual_index_0001_02.col_money from t_ai_virtual_index_0001_01 left join t_ai_virtual_index_0001_02 on t_ai_virtual_index_0001_01.col_int = t_ai_virtual_index_0001_02.col_int
where t_ai_virtual_index_0001_01.col_text like 'V_text_2999%' order by t_ai_virtual_index_0001_01.col_int desc limit 20;

--step16:删除索引4 expect:删除索引4成功
select * from hypopg_reset_index();

--step17:查询现有索引 expect:返回为空
select * from hypopg_display_index();

--step16:清理环境 expect:清理环境成功
drop table t_ai_virtual_index_0001_01;
drop table t_ai_virtual_index_0001_02;
drop procedure p_virtual_index_0001;