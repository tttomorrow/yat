-- @testpoint: 创建model，使用不同字符类型命名,部分测试点合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0004;
create table t_model_tab_0004(id int, second_attack int, treatment int,  trait_anxiety int);
insert into t_model_tab_0004 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 创建model,以保留关键字命名;expect: 合理报错
create model ASYMMETRIC  using logistic_regression features treatment,trait_anxiety target second_attack  from t_model_tab_0004;

--step3: 创建model,以已存在model名命名;expect: 合理报错
create model m_model_0004  using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0004;
create model m_model_0004  using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0004;

--step4: 创建model,以已存在的表名命名;expect: 创建成功
create model t_model_tab_0004  using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0004;

--step5: 查找系统表的model名;expect: 返回新建model的modelname值
select modelname from gs_model_warehouse;

--step6: 创建model,以_命名;expect: 创建成功
create model  _ using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0004;

--step8: 查找系统表的model名;expect: 返回_
select modelname from gs_model_warehouse order by modelname;

--step9: 清理环境;expect: 清理环境成功
drop model m_model_0004;
drop model t_model_tab_0004;
drop model _;
drop table t_model_tab_0004;