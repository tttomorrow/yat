-- @testpoint: kmeans创建mode带正确的超参切换schema

--step1: 创建表并插入数据;expect: 创建表并插入数据成功
drop table if exists t_model_tab_0048;
create table t_model_tab_0048(id integer not null,"position" double precision[] not null,closest_centroid integer not null, l1_distance double precision not null, l2_distance double precision not null,l2_squared_distance double precision not null,linf_distance double precision not null );
insert into t_model_tab_0048 values (214,'{82.2331969052000034,52.153098620199998,64.0347866000999933,-.325498647699999981,-64.6012147075999947,81.5499670644999952,59.6012626708999989}',3,10.0679804558999992,4.35061551650000012,18.9278551126999999,2.38475523010000019);

--step2: 创建schema并切换;expect: 创建schema成功,切换成功
drop schema if exists s_schema_0048;
create schema s_schema_0048;
set current_schema=s_schema_0048;

--step3: kmeans创建mode;expect: 创建成功
create model m_model_kmeans_schema_0048 using kmeans from(select position from public.t_model_tab_0048) with num_features = 7;

--step4: 切换schema为public,查询系统表中的 hyperparametersvalues;expect: 切换schema成功,返回hyperparametersvalues的值
set current_schema=public;
select hyperparametersvalues from gs_model_warehouse where modelname='m_model_kmeans_schema_0048';

--step5: 清理环境;expext: 清理成功
drop table t_model_tab_0048;
drop model m_model_kmeans_schema_0048;
drop schema s_schema_0048;