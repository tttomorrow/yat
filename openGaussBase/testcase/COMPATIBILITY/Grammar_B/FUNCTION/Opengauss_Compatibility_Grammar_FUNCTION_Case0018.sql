-- @testpoint: 时间函数utc_date功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入utc_date正常执行结果;expect:成功
insert into func_test(functionName, result) values('UTC_DATE', UTC_DATE);
insert into func_test(functionName, result) values('UTC_DATE()', UTC_DATE());

--step3:插入非法入参下utc_date执行结果;expect:合理报错
insert into func_test(functionName, result) values('UTC_DATE(1)', UTC_DATE(1));

--step4:查看utc_date函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;