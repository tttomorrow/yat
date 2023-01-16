-- @date: 2023-01-01
-- @testpoint: 使用distinctrow查询表数据
-- @history  ：Modifyed by zhangao 2023-01-02：适配最新代码

--step1:创建普通行存表;expect:成功
drop table if exists t_b_grammar_0002;
create table t_b_grammar_0002(id int,name varchar(20),age int,stuno int)engine =INNODB;

--step2:插入数据;expect:成功
insert t_b_grammar_0002 value(1,'zhangsan',18,23);
insert t_b_grammar_0002 value(2,'lisi',19,24);
insert t_b_grammar_0002 value(3,'wangwu',18,25);
insert t_b_grammar_0002 value(4,'zhaoliu',18,26);
insert t_b_grammar_0002 value(5,'zhangsan',18,27);
insert t_b_grammar_0002 value(6,'wangwu',20,28);

--step3:使用distinctrow,对一列去重;expect:成功(4 rows)
select distinctrow name from t_b_grammar_0002 order by name;

--step4:使用distict,对一列去重;expect:成功(4 rows),结果和step3一样
select distinct name from t_b_grammar_0002;

--step5:清理环境;expect:成功
drop table if exists t_b_grammar_0002;

