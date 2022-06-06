-- @testpoint: 使用不同算子创建model

--step1: 建表1并插入数据;expect: 建表1并插入数据成功
drop table if exists t_model_tab1_0008;
create table t_model_tab1_0008(id int, second_attack int, treatment int,  trait_anxiety int);
insert into t_model_tab1_0008 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 建表2并插入数据;expect: 建表2并插入数据成功
drop table if exists t_model_tab2_0008;
create table t_model_tab2_0008(id integer not null,
    "position" double precision[] not null,
    closest_centroid integer not null,
    l1_distance double precision not null,
    l2_distance DOUBLE PRECISION NOT NULL,
    l2_squared_distance double precision not null,
    linf_distance double precision not null );
insert into t_model_tab2_0008 values (214,'{82.2331969052000034,-52.153098620199998,-64.0339866000999933,-.325498639699999981,-64.6012142075999947,-81.5499670644999952,59.6012626708999989}',3,10.0679804578999992,4.35061571650000012,	18.9278571126999999,2.38415523010000019);

--step3: 建表3并插入数据;expect: 建表3并插入数据成功
drop table if exists t_model_tab3_0008;
create table t_model_tab3_0008(id int,tax int,bedroom int,bath float,price int,size int,lot int);
insert into t_model_tab3_0008 values (1,590,2,1,5000,770,22100),(2,1050,3,2,85000,1410,12000),(3,20,3,1,22500,1060,500),(4,870,2,2,90000,1300,17500),(5,1320,3,2,33000,1500,30000),(6,1350,3,100,90500,820,25700),(7,2790,3,2.5,260000,2130,25000),(8,680,2,1,142500,1170,22000),(9,1840,3,2,160000,1500,19000),(10,3680,4,2,240000,2790,20000),(11,1660,3,1,87000,1030,17500),(12,1620,3,2,118600,1250,20000),(13,3100,3,2,140000,1760,38000),(14,2070,2,3,148000,1550,14000),(15,650,3,1.5,65000,1450,12000);

--step4: 使用不同算子创建model;expect: 均创建成功
create model m_model_logistic_regression_0008 using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab1_0008;

create model m_model_kmeans_0008 using kmeans features position from t_model_tab2_0008 with num_features = 7;

create model m_model_linear_regression_0008 using linear_regression features 1,tax,bath,size target price from t_model_tab3_0008;

create model m_model_features_svm_0008 using svm_classification features treatment,trait_anxiety target second_attack from t_model_tab1_0008 with lambda=100;

--step5: 查找系统表的model名;expect: 返回m_model_logistic_regression_0008,m_model_kmeans_0008  ,m_model_linear_regression_0008 ,m_model_svm_0008
select modelname from gs_model_warehouse order by modelname;

--step6: 清理环境;expect: 清理环境成功
drop model m_model_logistic_regression_0008;
drop model m_model_kmeans_0008;
drop model m_model_linear_regression_0008;
drop model m_model_features_svm_0008;
drop table t_model_tab1_0008;
drop table t_model_tab2_0008;
drop table t_model_tab3_0008;