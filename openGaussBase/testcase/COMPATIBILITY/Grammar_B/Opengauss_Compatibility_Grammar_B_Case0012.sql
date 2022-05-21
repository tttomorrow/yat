-- @testpoint: 普通表插入数据，省略into
--testpoint1:
--step1:创建普通行存表;expect:成功
drop table if exists tb_b_grammar_0012;
create table tb_b_grammar_0012(a text(10),b mediumtext, c serial) engine =case0012;
--step2:插入数据一条数据;expect:成功
insert tb_b_grammar_0012 values('测试1','测试2*&^',default);
--step3:查询;expect:成功
select * from tb_b_grammar_0012;
--step4:插入多条数据;expect:成功
insert tb_b_grammar_0012 values(generate_series(1,10000),'col'||generate_series(1,10000),default);
--step5:查询;expect:成功
select count(*) from tb_b_grammar_0012;
truncate table tb_b_grammar_0012;
--step6:插入值中含单引号;expect:成功
insert tb_b_grammar_0012 values('汤姆','tom''s toys',default);
--step7:查询;expect:成功
select * from tb_b_grammar_0012;

--testpoint2:
--step1:创建临时表;expect:成功
drop table if exists tb_b_grammar_0012_02;
create temp table tb_b_grammar_0012_02(a text(10),b tinytext,c mediumtext,d longtext)engine =临时表;
--step2:插入数据，省略into;expect:成功
insert tb_b_grammar_0012_02 values('测试1','测试2*&^','测试3','测试4');

--testpoint3:
--step1:创建ustore表;expect:成功
drop table if exists tb_b_grammar_0012_03;
create temp table tb_b_grammar_0012_03(a text(10),b tinytext,c mediumtext,d longtext)with (storage_type=ustore)engine =引擎;
--step2:省略into;expect:成功
insert tb_b_grammar_0012_03 values('测试1','测试2*&^','测试3','测试4');
--step3:清理环境;expect:成功
drop table if exists tb_b_grammar_0012;
drop table if exists tb_b_grammar_0012_02;
drop table if exists tb_b_grammar_0012_03;
