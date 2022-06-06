-- @testpoint: logistic_regression创建mode带错误的超参optimizer,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0056 ;
create table t_model_tab_0056(id integer not null,second_attack integer,treatment integer,trait_anxiety integer );
insert into t_model_tab_0056 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 建表1并插入数据;expect: 建表1并插入数据成功
drop table if exists t_model_tab1_0056;
create table t_model_tab1_0056(id integer not null,"position" double precision[] not null,closest_centroid integer not null,l1_distance double precision not null,l2_distance double precision not null,l2_squared_distance double precision not null,linf_distance double precision not null );
insert into t_model_tab1_0056 values(214,'{82.2331969052000034,52.153098620199998,64.0339866000999933,-.325498639699999981,-64.6012142075699947,81.5499670644999952,56.6012626708999989}',3,10.0679804578999992,4.35061571650000012,18.9278571126999999,2.38415523010000019);

--step3: logistic_regression创建mode带错误的超参optimizer;expect: 创建失败，报错提示optimizer参数值错误
create model m_model_wrong_optimizer_0056 using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0056   with optimizer='az';

--step4: 清理环境;expext: 清理成功
drop table t_model_tab_0056;
drop table t_model_tab1_0056;