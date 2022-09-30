-- @testpoint: 插入数据,value后的值测试
--step1:创建普通行存表;expect:成功
drop table if exists tb_b_grammar_0015;
create table tb_b_grammar_0015(a text(10),b timestamp default current_timestamp, c double default 123.56) engine =myisam;
--step2:插入数据,值含表达式及默认值;expect:成功
insert tb_b_grammar_0015 value('测试1',current_timestamp,default);
select a from tb_b_grammar_0015;
--step3:插入多条;expect:成功
insert tb_b_grammar_0015 value(upper('lower'),current_timestamp,default),(lower('TRE'),current_timestamp,default);
--step4:查询;expect:成功
select a from tb_b_grammar_0015;
--step5:清理环境;expect:成功
drop table if exists tb_b_grammar_0015;
