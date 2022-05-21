-- @testpoint: 使用已有表数据给新表插入数据，省略into
--step1:创建2张表;expect:成功
drop table if exists tb_b_grammar_0013;
create table tb_b_grammar_0013(a text(10),b mediumtext, c serial) engine =表1;
drop table if exists tb_b_grammar_0013_01;
create table tb_b_grammar_0013_01(a text(10),b mediumtext, c serial) engine =表2;

--step2:给表1插入数据;expect:成功
insert tb_b_grammar_0013 values (generate_series(1,10000),'col'||generate_series(1,10000),default);

--step3:复制表1数据给表2;expect:成功
insert tb_b_grammar_0013_01 select * from tb_b_grammar_0013;

--step4:查询表2数据;expect:成功
select count(*) from tb_b_grammar_0013_01;

--step5:清空表2数据;expect:成功
delete tb_b_grammar_0013_01;
insert tb_b_grammar_0013_01 values(1,2,default);

--step6:清理环境;expect:成功
drop table if exists tb_b_grammar_0013;