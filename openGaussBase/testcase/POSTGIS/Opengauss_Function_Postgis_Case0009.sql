-- @testpoint: 验证integer,text,bytea,timestamp with time zone类型(不合理)的应用,合理报错

--step1:创建表   expect:成功
drop table if exists t_postgis_0008 cascade;
create table t_postgis_0008 (
    smflag integer,
    smversion integer,
    smminorversion integer,
    smdsdescription text,
    smprojectinfo bytea,
    smlastupdatetime timestamp with time zone default current_timestamp,
    smversiondate integer);

--step2:插入不合理数据   expect:失败，合理报错
insert into t_postgis_0008 values(21474836473,1,2,'text:smdsdescription',E'\\xBCDBCD','2020-8-25 pst',4);

insert into t_postgis_0008 values(1,2,3,'text:smdsdescription',E'\\xBCD',default,4);

insert into t_postgis_0008 values(1,2,3,'text:smdsdescription',E'\\xBCDE','2020-8-25',4);

--step3:查看数据   expect:数据为空
select * from t_postgis_0008;

--step4:清理环境   expect:成功
drop table t_postgis_0008;
