-- @testpoint: 创建model，二分类任务target列指定列超过两类结果,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0020;
create table t_model_tab_0020(id int,second_attack int,treatment int,trait_anxiety int);
insert into t_model_tab_0020 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 创建model,指定训练模型目标是表的列名;expect: 合理报错
create model m_model_target_column_0020 using logistic_regression features treatment,second_attack target trait_anxiety from t_model_tab_0020;

--step3：清理环境;expect: 清理环境成功
drop table t_model_tab_0020;