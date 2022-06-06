-- @testpoint: 外部调用package声明的公用函数

--step1:建表并插入数据 expect:成功
drop table if exists t_package_0011;
create table t_package_0011(core int,name varchar(10));
insert into t_package_0011 values(50,'test'),(100,'tom'),(50,'john'),(60,'kitty');

--step2:声明包规格 expect:成功
create or replace package p_test_0011 is
function f_package_0011 return varchar;
end p_test_0011;
/

--step3:定义包体 expect:成功
create or replace package body p_test_0011 is
function f_package_0011 return varchar is
declare
	v_sql_statement varchar(2000);
begin
    v_sql_statement := (select name from t_package_0011 where core = 100);
	return v_sql_statement;
end;
end p_test_0011;
/

--step4:创建存储过程,调用包内函数 expect:成功
create or replace procedure p_package_0011 (out var1 varchar(10))
is
begin
	var1 := (select p_test_0011.f_package_0011());
end;
/

--step5:调用存储过程 expect:返回package中函数执行结果
call p_package_0011(null);

--step6:清理环境 expect:成功
drop package p_test_0011;
drop procedure p_package_0011;