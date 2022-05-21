-- @testpoint: 创建model,不影响对基础表做ddl和dml操作

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0001;
create table t_model_tab_0001(id int,second_attack int,treatment int,trait_anxiety int);
insert into t_model_tab_0001 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: 创建model;expect: 创建成功
create model m_model_ddl_tab_0001 using logistic_regression features treatment,trait_anxiety target second_attack  from t_model_tab_0001;

--step3: 查找系统表的model名;expect: 返回m_model_ddl_tab_0001
select modelname from gs_model_warehouse;

--step4: 对基础表进行写入操作;expect: 写入成功,不影响基础表操作
insert into t_model_tab_0001 values(8,270,13,2.6);

--step5: 再次查找系统表的model名;expect: 返回创建model的modelname值
select modelname from gs_model_warehouse order by modelname;

--step6: 清理环境;expect: 清理环境成功
drop model m_model_ddl_tab_0001;
drop table t_model_tab_0001;