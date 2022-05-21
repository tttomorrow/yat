-- @testpoint: NVARCHAR存储空间：最大为10MB 部分测试点合理报错

--step1:建表; expect:成功
drop table if exists t_nvarchar_0001 cascade;
create table t_nvarchar_0001(
c_nvarchar nvarchar(10485760));

--step2:插入值10*1024*1024; expect:成功
insert into t_nvarchar_0001(c_nvarchar) values(lpad('a', 1024*10*1024, 'x')::nvarchar);
select length(c_nvarchar) from t_nvarchar_0001;

--step3:插入值10*1024*1024-1; expect:成功
insert into t_nvarchar_0001(c_nvarchar) values(lpad('a', 1024*10*1024-1, 'x')::nvarchar);
select length(c_nvarchar) from t_nvarchar_0001;

--step4:插入值10*1024*1024+1; expect:失败
insert into t_nvarchar_0001(c_nvarchar) values(lpad('a', 1024*10*1024+1, 'x')::nvarchar);
select length(c_nvarchar) from t_nvarchar_0001;

--step5:清理环境; expect:成功
drop table if exists t_nvarchar_0001 cascade;