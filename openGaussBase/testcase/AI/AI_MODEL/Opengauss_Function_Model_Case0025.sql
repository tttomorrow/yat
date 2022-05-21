-- @testpoint: 创建model，target指定不同训练模型目标,部分用例合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0025;
create table t_model_tab_0025(id int,second_attack int,treatment int,trait_anxiety int);
insert into t_model_tab_0025 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 创建model，target指定训练模型目标是表带_的列名;expect: 创建model成功
create model m_model_target_column_0025 using logistic_regression features trait_anxiety,treatment target second_attack from t_model_tab_0025;

--step3: 创建model，target指定训练模型目标是表不存在的列名;expect: 报错提示指定的列不存在
create model m_model_target_non_column_0025 using logistic_regression features rait_anxiety,treatment target column1 from t_model_tab_0025;

--step4: 创建model，target指定训练模型目标是表达式;expect: 创建model成功
create model m_model_target_expression_0025 using svm_classification features second_attack target trait_anxiety > 10 from t_model_tab_0025;

--step5: 查找系统表;expect: 返回新建model的modelname
select modelname from gs_model_warehouse order by modelname;

--step6:清理环境;expect: 清理环境成功
drop model m_model_target_column_0025;
drop model m_model_target_expression_0025;
drop table t_model_tab_0025;
