-- @testpoint: 创建model,gd算子features指定ARRAY类型,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0050;
create table t_model_tab_0050(id integer not null, second_attack integer ,treatment integer ,trait_anxiety integer );
insert into t_model_tab_0050 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 创建model,gd算子features指定ARRAY类型;expect: 创建失败，报错
create model m_fertures_gd_array_0050 using logistic_regression features array[treatment,trait_anxiety] target second_attack from t_model_tab_0050;

--step3: 清理环境;expext: 清理成功
drop table t_model_tab_0050;