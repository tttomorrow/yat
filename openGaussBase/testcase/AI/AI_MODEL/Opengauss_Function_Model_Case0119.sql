-- @testpoint: kmeans创建mode,带不正确的超参tolerance,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0119;
create table t_model_tab_0119(id integer not null,
    "position" double precision[] not null,
    closest_centroid integer not null,
    l1_distance double precision not null,
    l2_distance double precision not null,
    l2_squared_distance double precision not null,
    linf_distance double precision not null );
insert into t_model_tab_0119 values (214,'{82.2331969052000034,-52.153098620199998,-64.0339866000999933,-.325498639699999981,-64.6011942075999947,-81.5499670644999952,59.6012626708999989}',3,10.0679804578999992,4.35061571650000012,	18.9278571126999999,2.38415523010000019);

--step2: kmeans创建mode,带不正确的超参tolerance;expect: 创建失败,报错提参数tolerance值错误
create model m_model_max_iterations_0119 using kmeans from ( select position from  t_model_tab_0119 ) with tolerance=0,num_features = 7;

create model m_model_max_iterations1_0119 using kmeans from ( select position from  t_model_tab_0119 ) with tolerance = 1.1,num_features = 7;

--step3: 清理环境;expext: 清理成功
drop table t_model_tab_0119;