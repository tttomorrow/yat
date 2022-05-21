-- @testpoint: 创建model，kmeans指定target列，合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0024;
create table t_model_tab_0024(id int,second_attack int,treatment int,trait_anxiety int);
insert into t_model_tab_0024 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 创建model,kmeans指定target列;expect: 报错提示target列无法指定
create model m_model_target_column_0024 using kmeans features treatment,trait_anxiety target second_attack from t_model_tab_0024;

--step3: 清理环境;expect: 清理环境成功
drop table t_model_tab_0024;