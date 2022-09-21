-- @testpoint: 时间函数to_days功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时to_days执行结果;expect:成功
insert into func_test(functionName,result) values('TO_DAYS(''2022-1-1'')',TO_DAYS('2022-1-1'));
insert into func_test(functionName,result) values('TO_DAYS(''44440101'')',TO_DAYS('44440101'));
insert into func_test(functionName,result) values('TO_DAYS(20000229)',TO_DAYS(20000229));
insert into func_test(functionName,result) values('TO_DAYS(''2022-1-1 1:1:1'')',TO_DAYS('2022-1-1 1:1:1'));
insert into func_test(functionName,result) values('TO_DAYS(''2022-2-2 2:2:2.0000015'')',TO_DAYS('2022-2-2 2:2:2.0000015'));
insert into func_test(functionName,result) values('TO_DAYS(''20220101010101'')',TO_DAYS('20220101010101'));
insert into func_test(functionName,result) values('TO_DAYS(20220101010101)',TO_DAYS(20220101010101));
insert into func_test(functionName,result) values('TO_DAYS(''20220101010101.000001'')',TO_DAYS('20220101010101.000001'));
insert into func_test(functionName,result) values('TO_DAYS(20220101010101.000002)',TO_DAYS(20220101010101.000002));
insert into func_test(functionName,result) values('TO_DAYS(''00000000000-1-1'')',TO_DAYS('00000000000-1-1'));
insert into func_test(functionName,result) values('TO_DAYS(''00000000000-00000000001-1'')',TO_DAYS('00000000000-00000000001-1'));
insert into func_test(functionName,result) values('TO_DAYS(''00000000000-00000000001-0000000001'')',TO_DAYS('00000000000-00000000001-0000000001'));
insert into func_test(functionName,result) values('TO_DAYS(''0000-1-1'')',TO_DAYS('0000-1-1'));
insert into func_test(functionName,result) values('TO_DAYS(''0000-1-1 00:00:00'')',TO_DAYS('0000-1-1 00:00:00'));
insert into func_test(functionName,result) values('TO_DAYS(''9999-12-31'')',TO_DAYS('9999-12-31'));
insert into func_test(functionName,result) values('TO_DAYS(''9999-12-31 23:59:59.999999'')',TO_DAYS('9999-12-31 23:59:59.999999'));

--step3:插入入参为数值格式的to_days执行结果;expect:非法数值格式合理报错
insert into func_test(functionName,result) values('TO_DAYS(1)',TO_DAYS(1));
insert into func_test(functionName,result) values('TO_DAYS(1)',TO_DAYS(1));
insert into func_test(functionName,result) values('TO_DAYS(001)',TO_DAYS(001));
insert into func_test(functionName,result) values('TO_DAYS(101)',TO_DAYS(101));
insert into func_test(functionName,result) values('TO_DAYS(0101)',TO_DAYS(0101));
insert into func_test(functionName,result) values('TO_DAYS(00101)',TO_DAYS(00101));
insert into func_test(functionName,result) values('TO_DAYS(000101)',TO_DAYS(000101));
insert into func_test(functionName,result) values('TO_DAYS(00000101)',TO_DAYS(00000101));
insert into func_test(functionName,result) values('TO_DAYS(00000101001)',TO_DAYS(00000101001));
insert into func_test(functionName,result) values('TO_DAYS(00000101000001)',TO_DAYS(00000101000001));
insert into func_test(functionName,result) values('TO_DAYS(01000001)',TO_DAYS(01000001));
insert into func_test(functionName,result) values('TO_DAYS(0101000001)',TO_DAYS(0101000001));
insert into func_test(functionName,result) values('TO_DAYS(00101000001)',TO_DAYS(00101000001));
insert into func_test(functionName,result) values('TO_DAYS(0000101000001)',TO_DAYS(0000101000001));

--step4:插入入参为特殊类型的to_days用例执行结果;expect:成功
insert into func_test(functionName,result) values('TO_DAYS(null)',TO_DAYS(null));
insert into func_test(functionName,result) values('TO_DAYS(date''2000-1-1'')',TO_DAYS(date'2000-1-1'));
insert into func_test(functionName,result) values('TO_DAYS(cast(''2022-2-2 2:2:2'' as datetime))',TO_DAYS(cast('2022-2-2 2:2:2' as datetime)));
insert into func_test(functionName,result) values('TO_DAYS(time''1:1:1'')',TO_DAYS(time'1:1:1'));
insert into func_test(functionName,result) values('TO_DAYS(time''25:0:0'')',TO_DAYS(time'25:0:0'));

--step5:插入非法入参时to_days用例执行结果;expect:合理报错
insert into func_test(functionName,result) values('TO_DAYS(true)',TO_DAYS(true));
insert into func_test(functionName,result) values('TO_DAYS(false)',TO_DAYS(false));
insert into func_test(functionName,result) values('TO_DAYS(''2022-1-32'')',TO_DAYS('2022-1-32'));
insert into func_test(functionName,result) values('TO_DAYS(''2022-13-1'')',TO_DAYS('2022-13-1'));
insert into func_test(functionName,result) values('TO_DAYS(''2022-2-2 2:2:60'')',TO_DAYS('2022-2-2 2:2:60'));
insert into func_test(functionName,result) values('TO_DAYS(''2022-2-2 2:60:2'')',TO_DAYS('2022-2-2 2:60:2'));
insert into func_test(functionName,result) values('TO_DAYS(''2022-2-2 24:2:2'')',TO_DAYS('2022-2-2 24:2:2'));
insert into func_test(functionName,result) values('TO_DAYS(''99999999999-1-1'')',TO_DAYS('99999999999-1-1'));

--step6:插入to_days涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName,result) values('TO_DAYS(''0000-0-0'')',TO_DAYS('0000-0-0'));
insert into func_test(functionName,result) values('TO_DAYS(''10000-1-1'')',TO_DAYS('10000-1-1'));
insert into func_test(functionName,result) values('TO_DAYS(''10000-1-1 00:00:00'')',TO_DAYS('10000-1-1 00:00:00'));

--step7:查看to_days函数执行结果是否正确;expect:成功
select * from func_test;

--step8:清理环境;expect:成功
drop table if exists func_test;