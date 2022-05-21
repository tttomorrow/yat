-- @testpoint: svm创建mode带超参seed最大值,超参seed超出最大值,部分测试点合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0096;
create table t_model_tab_0096(id integer not null,second_attack integer,treatment integer,trait_anxiety integer );
insert into t_model_tab_0096 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: svm创建mode带超参seed最大值;expect: 创建成功
create model m_model_max_seed_0096 using svm_classification features treatment,trait_anxiety target second_attack from t_model_tab_0096  with seed = 2147483647;

--step3: 查找系统表;expect: 返回内容中含seed的值
select hyperparametersvalues from gs_model_warehouse where modelname='m_model_max_seed_0096';

--step4: 查找系统表;expect: 返回创建model的modelname值m_model_max_seed_0096
select modelname from gs_model_warehouse order by modelname;

--step5: svm创建mode带超出超参seed最大值;expect: 创建失败,报错提示参数seed值错误
create model m_model_max_seed1_0096 using svm_classification  features treatment,trait_anxiety target second_attack from t_model_tab_0096  with seed = 2147483648;

--step6: 清理环境;expext: 清理成功
drop table t_model_tab_0096;
drop model m_model_max_seed_0096;