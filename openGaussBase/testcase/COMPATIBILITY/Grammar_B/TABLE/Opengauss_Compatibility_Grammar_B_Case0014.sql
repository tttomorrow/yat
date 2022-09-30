-- @testpoint: 插入数据，使用value和values,部分测试点合理报错
--step1:创建普通行存表;expect:成功
drop table if exists tb_b_grammar_0014;
create table tb_b_grammar_0014(a text(10),b mediumtext, c serial) engine =引擎;

--省略into且使用value
--step2:插入数据，表名不存在;expect:报错
insert tb_b_grammar_0014_adyuy value('测试1','测试',1);
--step3:插入数据一条数据;expect:成功
insert tb_b_grammar_0014 value('测试1','测试2*&^',default);
--step4:插入多条数据;expect:成功
insert tb_b_grammar_0014 value (generate_series(1,10000),'col'||generate_series(1,10000),default);
--step5:插入值中含单引号;expect:成功
insert tb_b_grammar_0014 value('汤姆','tom''s toys',default);
--step6:省略into使用values;expect:成功
insert tb_b_grammar_0014 values('杰克','jack''s toys',default);
--step7:添加into且使用value;expect:成功
insert into tb_b_grammar_0014 value('测试1','测试',1);
--step8:添加into且使用values;expect:成功
insert into tb_b_grammar_0014 values('测试s','测试',1);
--step9:清理环境;expect:成功
drop table if exists tb_b_grammar_0014;