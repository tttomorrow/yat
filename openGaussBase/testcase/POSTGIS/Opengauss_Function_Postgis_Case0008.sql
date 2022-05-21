-- @testpoint: 验证integer,text,bytea,timestamp with time zone类型(合理)的应用

--step1:创建表   expect:成功
drop table if exists t_postgis_0007 cascade;
create table t_postgis_0007 (
    smflag integer,
    smversion integer,
    smminorversion integer,
    smdsdescription text,
    smprojectinfo bytea,
    smlastupdatetime timestamp with time zone default '2021-11-19',
    smversiondate integer);

--step2:插入数据   expect:成功
insert into t_postgis_0007 values(1,2,3,'text:smdsdescription',e'\\xbcdbcd','2020-8-25 pst',4);
insert into t_postgis_0007 values(1,2,3,'text:smdsdescription',E'\\xBC',default,4);

--step3:查看数据   expect:成功
select * from t_postgis_0007;

--step4:清理环境   expect:成功
drop table t_postgis_0007;
