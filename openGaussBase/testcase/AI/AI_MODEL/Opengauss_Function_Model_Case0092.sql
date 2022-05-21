-- @testpoint: svm创建mode带超参tolerance

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0092;
create table t_model_tab_0092(id integer not null,second_attack integer,treatment integer,trait_anxiety integer );
insert into t_model_tab_0092 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: svm创建mode带超参tolerance;expect: 创建成功
create model m_model_tolerance_0092 using svm_classification features treatment,trait_anxiety target second_attack from t_model_tab_0092 with tolerance =150;

--step3: 查找系统表;expect: 返回内容中含tolerance的值
select hyperparametersvalues from gs_model_warehouse where modelname='m_model_tolerance_0092';

--step4: 查找系统表;expect: 返回创建model的modelname值m_model_tolerance_0092
select modelname from gs_model_warehouse order by modelname;

--step5: 清理环境;expext: 清理成功
drop table t_model_tab_0092;
drop model m_model_tolerance_0092;