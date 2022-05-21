-- @testpoint: kmeans创建mode，带正确的超参tolerance

--step1: 创建表并插入数据;expect: 创建表并插入数据成功
drop table if exists t_model_tab_0041;
create table t_model_tab_0041(id integer not null,"position" double precision[] not null,closest_centroid integer not null, l1_distance double precision not null, l2_distance double precision not null,l2_squared_distance double precision not null,linf_distance double precision not null );
insert into t_model_tab_0041 values (214,'{82.2331969052000034,52.153098620199998,64.0341866000999933,-.325498641699999981,-64.6012142075999947,81.5499670644999952,59.6012626708999989}',3,10.0679804558999992,4.35061551650000012,18.9278551126999999,2.38415523010000019);

--step2: kmeans创建mode带正确的超参tolerance;expect: 创建成功
create model m_model_kmeans_tolerance_0041 using kmeans from (select position from t_model_tab_0041 ) with tolerance=0.1,num_features = 7;

--step3: 查询系统表中的 hyperparametersvalues;expect: 返回的内容中含设置的tolerance的值
select hyperparametersvalues from gs_model_warehouse where modelname='m_model_kmeans_tolerance_0041';

--step4: 清理环境;expext: 清理成功
drop table t_model_tab_0041;
drop model m_model_kmeans_tolerance_0041;