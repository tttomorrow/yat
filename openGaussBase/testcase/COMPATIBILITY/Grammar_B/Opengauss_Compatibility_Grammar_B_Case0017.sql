-- @testpoint: 查询表数据，使用distinctrowrow on，部分测试点合理报错
--step1:建表;expect:成功
drop table if exists tb_grammar0017;
create table tb_grammar0017(id int,name text, subject text, score numeric)engine 去重;
--step2:插入数据;expect:成功
insert tb_grammar0017 value(1,'killy','数学',99.5),(2,'killy','语文',89.5),(3,'killy','英语',79.5),(4,'killy','物理',99.5),(5,'张三','数学',89.5),(6,'张三','语文',99.5),(7,'张三','英语',79.5),(8,'张三','物理',89.5);
--step3:查询当前数据;expect:成功
select * from tb_grammar0017;
--step4:取出每门课程的第一名;expect:成功（先根据subject分组，score desc决定每一组的内部排序，最终决定每组取谁）
 select distinctrow on(subject)id,name,subject,score from tb_grammar0017 order by subject,score desc;
 select distinctrow on(subject / 10)id,name,subject,score from tb_grammar0017 order by (subject / 10);
--step5:排序列顺序不对，;expect:合理报错
 select distinctrow on(subject)id,name,subject,score from tb_grammar0017 order by score desc,subject;
--step6:distinctrowrow on（括号里跟2个参数）;expect:成功
select distinctrow on(id,subject)id,name,subject,score from tb_grammar0017 order by id, subject,score desc;
--step7:清理环境;expect:成功
drop table if exists tb_grammar0017;
