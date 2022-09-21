-- @testpoint: 时间函数timestampadd(入参为datetime格式)功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入timestampadd正常执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(YEAR,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(YEAR,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(MONTH,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(MONTH,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(WEEK,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(WEEK,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(DAY,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(DAY,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(HOUR,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(HOUR,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(MINUTE,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(MINUTE,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1,''2022-07-27 08:30:00'')', TIMESTAMPADD(SECOND,1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1,''2022-07-27 08:30:00'')', TIMESTAMPADD(SECOND,-1,'2022-07-27 08:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,''2022-07-27 -01:30:00'')', TIMESTAMPADD(DAY,1,'2022-07-27 -01:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,''2022-07-27 -12:30:00'')', TIMESTAMPADD(HOUR,1,'2022-07-27 -12:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1,''2022-07-27 08:30:-01'')', TIMESTAMPADD(SECOND,-1,'2022-07-27 08:30:-01'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1, 20220727083000)', TIMESTAMPADD(SECOND,-1, 20220727083000));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1, 20220727083000.000001)', TIMESTAMPADD(SECOND,-1, 20220727083000.000001));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1,''2022-07-27 08:-59:00'')', TIMESTAMPADD(MINUTE,-1,'2022-07-27 08:-59:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1,''2022-07-27 -01:-30:00'')', TIMESTAMPADD(YEAR,-1,'2022-07-27 -01:-30:00'));

insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,''2022-07-27 23:30:00'')', TIMESTAMPADD(HOUR,1,'2022-07-27 23:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1,''2022-07-27 00:30:00'')', TIMESTAMPADD(HOUR,-1,'2022-07-27 00:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1,''2022-07-27 08:59:59'')', TIMESTAMPADD(MINUTE,1,'2022-07-27 08:59:59'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1,''2022-07-27 08:00:00'')', TIMESTAMPADD(MINUTE,-1,'2022-07-27 08:00:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1,''2022-07-27 08:30:59'')', TIMESTAMPADD(SECOND,1,'2022-07-27 08:30:59'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1,''2022-07-27 00:00:00'')', TIMESTAMPADD(SECOND,-1,'2022-07-27 00:00:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,0.001,''2022-07-27 08:30:59.999'')', TIMESTAMPADD(SECOND,0.001,'2022-07-27 08:30:59.999'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-0.001,''2022-07-27 00:00:00'')', TIMESTAMPADD(SECOND,-0.001,'2022-07-27 00:00:00'));

--step3:插入timestampadd涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,''9999-12-31 23:59:59'')', TIMESTAMPADD(DAY,1,'9999-12-31 23:59:59'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''0001-01-01 00:00:00'')', TIMESTAMPADD(DAY,-1,'0001-01-01 00:00:00'));

--step4:插入入参为特殊类型的timestampadd用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,true,''2022-04-05'')', TIMESTAMPADD(HOUR,true,'2022-04-05'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,B''11'',''2022-04-05'')', TIMESTAMPADD(HOUR,B'11','2022-04-05'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,date''2022-04-05'')', TIMESTAMPADD(HOUR,1,date'2022-04-05'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,cast(''2022-04-05'' as datetime))', TIMESTAMPADD(day,1,cast('2022-04-05' as datetime)));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,time''14:30:00'')', TIMESTAMPADD(day,1,time'14:30:00'));

--step5:插入非法入参时timestampadd执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1,''2022-07-27 24:30:00'')', TIMESTAMPADD(YEAR,1,'2022-07-27 24:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1,''2022-07-27 26:61:60'')', TIMESTAMPADD(MONTH,1,'2022-07-27 26:61:60'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1,''2022-07-27 08:60:60'')', TIMESTAMPADD(MONTH,-1,'2022-07-27 08:60:60'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''2022-07-27 25:30:00'')', TIMESTAMPADD(DAY,-1,'2022-07-27 25:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1,''2022-07-27 25:30:00'')', TIMESTAMPADD(HOUR,-1,'2022-07-27 25:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1,''2022-07-27 08:61:00'')', TIMESTAMPADD(MINUTE,1,'2022-07-27 08:61:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1,''2022-07-27 08:30:60'')', TIMESTAMPADD(SECOND,1,'2022-07-27 08:30:60'));

--step6:查看timestampadd函数执行结果是否正确;expect:成功
select * from func_test;

--step7:清理环境;expect:成功
drop table if exists func_test;