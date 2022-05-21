-- @testpoint: 创建快照与创建model结合,使用不同的算子创建model

--step1: 建表1并插入数据;expect: 建表1并插入数据成功
drop table if exists t_model_tab_0099;
create table t_model_tab_0099(id integer not null,second_attack integer ,treatment integer ,trait_anxiety integer );
insert into t_model_tab_0099 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 建表2并插入数据;expect: 建表2并插入数据成功
drop table if exists t_model_tab1_0099;
create table t_model_tab1_0099(id integer not null,"position" double precision[] not null,closest_centroid integer not null, l1_distance double precision not null, l2_distance double precision not null,l2_squared_distance double precision not null,linf_distance double precision not null );
insert into t_model_tab1_0099 values (214,'{82.2331969052000034,52.153098620199998,64.0339866000999933,-.325498639699999981,-64.6012142075999947,81.5499670644999952,59.6012626708999989}',3,10.0679804558999992,4.35061551650000012,18.9278551126999999,2.38415523010000019),

--step3: 建表3并插入数据;expect: 建表3并插入数据成功
drop table if exists t_model_tab2_0099;
create table t_model_tab2_0099(id int,tax int,bedroom int,bath float,price int, size int,lot int);
insert into t_model_tab2_0099 values (1,590,2,1,5000,770,22100),(2,1050,3,2,85000,1410,12000),(3,20,3,1,22500,1060,500),(4,870,2,2,90000,1300,17500),(5,1320,3,2,33000,1500,30000),(6,1350,3,100,90500,820,25700),(7,2790,3,2.5,260000,2130,25000),(8,680,2,1,142500,1170,22000),(9,1840,3,2,160000,1500,19000),(10,3680,4,2,240000,2790,20000),(11,1660,3,1,87000,1030,17500),(12,1620,3,2,118600,1250,20000),(13,3100,3,2,140000,1760,38000),(14,2070,2,3,148000,1550,14000),(15,650,3,1.5,65000,1450,12000);

--step4: 创建快照;expect: 创建成功
create snapshot s_snapshot_s1@1.0 comment is 'first version' as select * from t_model_tab_0099;

--step5: 创建训练集与测试集;expect: 创建训练集与测试集成功
sample snapshot s_snapshot_s1@1.0  stratify by second_attack as _test at ratio .2, as _train at ratio .8 comment is 'training';

--step6: 使用logistic_regression算子创建model;expect: 创建成功
create model m_model_snapshot_0099 using logistic_regression features treatment,trait_anxiety target second_attack from s_snapshot_s1_train@1.0;

--step7: 创建快照;expect: 创建成功
create snapshot s_snapshot_s2@1.0 comment is 'first version' as select * from t_model_tab1_0099;

--step8: 创建训练集与测试集;expect: 创建训练集与测试集成功
sample snapshot s_snapshot_s2@1.0  stratify by position as _test at ratio .2, as _train at ratio .8 comment is 'training';

--step9: 使用kmeans算子创建model;expect: 创建成功
create model m_model_snapshot1_0099 using kmeans features position from (select  position,l1_distance,closest_centroid from s_snapshot_s2_train@1.0) with  max_iterations =1,num_features = 7;

--step10: 创建快照;expect: 创建成功
create snapshot s_snapshot_s3@1.0 comment is 'first version' as select * from t_model_tab2_0099;

--step11: 创建训练集与测试集;expect: 创建训练集与测试集成功
sample snapshot s_snapshot_s3@1.0  stratify by price as _test at ratio .2, as _train at ratio .8 comment is 'training';

--step12: 使用linear_regression算子创建model;expect: 创建成功
create model m_model_snapshot2_0099 using linear_regression features 1,tax,bath,size target price from t_model_tab2_0099;

--step13: 创建快照;expect: 创建成功
create snapshot s_snapshot_s4@1.0 comment is 'first version' as select * from t_model_tab_0099;

--step14: 创建训练集与测试集;expect: 创建训练集与测试集成功
sample snapshot s_snapshot_s4@1.0 stratify by second_attack as _test at ratio .2, as _train at ratio .8 comment is 'training';

--step15: 使用svm算子创建model;expect: 创建成功
create model m_model_snapshot3_0099 using svm_classification features treatment,trait_anxiety target second_attack from s_snapshot_s4_train@1.0;


--step16: 清理环境;expect: 清理成功
purge snapshot s_snapshot_s1_train@1.0;
purge snapshot s_snapshot_s1_test@1.0;
purge snapshot s_snapshot_s1@1.0;
purge snapshot s_snapshot_s2_train@1.0;
purge snapshot s_snapshot_s2_test@1.0;
purge snapshot s_snapshot_s2@1.0;
purge snapshot s_snapshot_s3_train@1.0;
purge snapshot s_snapshot_s3_test@1.0;
purge snapshot s_snapshot_s3@1.0;
purge snapshot s_snapshot_s4_train@1.0;
purge snapshot s_snapshot_s4_test@1.0;
purge snapshot s_snapshot_s4@1.0;
drop table t_model_tab_0099;
drop table t_model_tab1_0099;
drop table t_model_tab2_0099;
drop model m_model_snapshot_0099;
drop model m_model_snapshot1_0099;
drop model m_model_snapshot2_0099;
drop model m_model_snapshot3_0099;