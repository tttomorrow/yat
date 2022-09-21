-- @testpoint: 时间函数to_seconds功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时to_seconds执行结果;expect:成功
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27'')', TO_SECONDS('2022-07-27'));
insert into func_test(functionName, result) values('TO_SECONDS(''20220727'')', TO_SECONDS('20220727'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27 15:25:30'')', TO_SECONDS('2022-07-27 15:25:30'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27 15:25:30.8888855'')', TO_SECONDS('2022-07-27 15:25:30.8888855'));
insert into func_test(functionName, result) values('TO_SECONDS(''20220727152530'')', TO_SECONDS('20220727152530'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27 15:25:30.8888854'')', TO_SECONDS('2022-07-27 15:25:30.8888854'));
insert into func_test(functionName, result) values('TO_SECONDS(050505)', TO_SECONDS(050505));
insert into func_test(functionName, result) values('TO_SECONDS(20220801)', TO_SECONDS(20220801));
insert into func_test(functionName, result) values('TO_SECONDS(20220801182030)', TO_SECONDS(20220801182030));
insert into func_test(functionName, result) values('TO_SECONDS(20220801182030.8888855)', TO_SECONDS(20220801182030.8888855));
insert into func_test(functionName, result) values('TO_SECONDS(''9999-12-31'')', TO_SECONDS('9999-12-31'));
insert into func_test(functionName, result) values('TO_SECONDS(''9999-12-31 23:59:59'')', TO_SECONDS('9999-12-31 23:59:59'));
insert into func_test(functionName, result) values('TO_SECONDS(''9999-12-31 23:59:59.999999'')', TO_SECONDS('9999-12-31 23:59:59.999999'));
insert into func_test(functionName, result) values('TO_SECONDS(''0000-01-01 00:00:00'')', TO_SECONDS('0000-01-01 00:00:00'));
insert into func_test(functionName, result) values('TO_SECONDS(''0000-01-01'')', TO_SECONDS('0000-01-01'));

--step3:插入入参为特殊类型的to_seconds用例执行结果;expect:成功
insert into func_test(functionName, result) values('TO_SECONDS(null)', TO_SECONDS(null));
insert into func_test(functionName, result) values('TO_SECONDS(date''2022-04-05'')', TO_SECONDS(date'2022-04-05'));
insert into func_test(functionName, result) values('TO_SECONDS(cast(''2022-04-05 14:35:00'' as datetime))', TO_SECONDS(cast('2022-04-05 14:35:00' as datetime)));
insert into func_test(functionName, result) values('TO_SECONDS(cast(''2022-04-05 14:35:00.888'' as datetime))', TO_SECONDS(cast('2022-04-05 14:35:00.888' as datetime)));
insert into func_test(functionName, result) values('TO_SECONDS(time''1:1:1'')', TO_SECONDS(time'1:1:1'));
insert into func_test(functionName, result) values('TO_SECONDS(time''25:00:00'')', TO_SECONDS(time'25:00:00'));

--step4:插入非法入参时to_seconds用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-32'')', TO_SECONDS('2022-07-32'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-13-27'')', TO_SECONDS('2022-13-27'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27 12:00:61'')', TO_SECONDS('2022-07-27 12:00:61'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27 12:61:00'')', TO_SECONDS('2022-07-27 12:61:00'));
insert into func_test(functionName, result) values('TO_SECONDS(''2022-07-27 25:00:00'')', TO_SECONDS('2022-07-27 25:00:00'));
insert into func_test(functionName, result) values('TO_SECONDS(true)', TO_SECONDS(true));

--step5:插入to_seconds涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TO_SECONDS(''10000-01-01'')', TO_SECONDS('10000-01-01'));
insert into func_test(functionName, result) values('TO_SECONDS(''0000-00-00'')', TO_SECONDS('0000-00-00'));
insert into func_test(functionName, result) values('TO_SECONDS(''0000-00-00 00:00:00'')', TO_SECONDS('0000-00-00 00:00:00'));

--step6:查看to_seconds函数执行结果是否正确;expect:成功
select * from func_test;

--step7:清理环境;expect:成功
drop table if exists func_test;