-- @testpoint: 测试select into语句中带有case when select子语句时给int数据类型赋值

--创建测试表
drop table if exists t_casewhen_002;
create table t_casewhen_002(id int,year int,month int,day int);
insert into t_casewhen_002 values (1,2018,6,30);

--创建匿名块
declare
    v_int int;
begin
    select (select case id when 1 then '1530331200' end from t_casewhen_002) into v_int from sys_dummy;
     raise info 'result:% ',v_int;
end;
/
--清理环境
drop table t_casewhen_002;