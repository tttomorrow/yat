-- @testpoint: 时间函数timestampadd(入参为date格式)功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入timestampadd正常执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1,''2022-07-27'')', TIMESTAMPADD(YEAR,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1,''2022-07-27'')', TIMESTAMPADD(YEAR,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1,''2022-07-27'')', TIMESTAMPADD(MONTH,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1,''2022-07-27'')', TIMESTAMPADD(MONTH,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,1,''2022-07-27'')', TIMESTAMPADD(WEEK,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,-1,''2022-07-27'')', TIMESTAMPADD(WEEK,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,''2022-07-27'')', TIMESTAMPADD(DAY,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''2022-07-27'')', TIMESTAMPADD(DAY,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,''2022-07-27'')', TIMESTAMPADD(HOUR,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1,''2022-07-27'')', TIMESTAMPADD(HOUR,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1,''2022-07-27'')', TIMESTAMPADD(MINUTE,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1,''2022-07-27'')', TIMESTAMPADD(MINUTE,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1,''2022-07-27'')', TIMESTAMPADD(SECOND,1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1,''2022-07-27'')', TIMESTAMPADD(SECOND,-1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1, 2022-07-27)', TIMESTAMPADD(SECOND,-1, 20220727));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,2,''2022-07-31'')', TIMESTAMPADD(MONTH,2,'2022-07-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1,''2020-02-29'')', TIMESTAMPADD(YEAR,1,'2020-02-29'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,3,''2019-12-31'')', TIMESTAMPADD(MONTH,3,'2019-12-31'));

insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1.1,''2022-07-27'')', TIMESTAMPADD(YEAR,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1.1,''2022-07-27'')', TIMESTAMPADD(YEAR,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1.6,''2022-07-27'')', TIMESTAMPADD(YEAR,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1.6,''2022-07-27'')', TIMESTAMPADD(YEAR,-1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1.1,''2022-07-27'')', TIMESTAMPADD(MONTH,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1.1,''2022-07-27'')', TIMESTAMPADD(MONTH,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1.6,''2022-07-27'')', TIMESTAMPADD(MONTH,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1.6,''2022-07-27'')', TIMESTAMPADD(MONTH,-1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,1.1,''2022-07-27'')', TIMESTAMPADD(WEEK,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,-1.1,''2022-07-27'')', TIMESTAMPADD(WEEK,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,1.6,''2022-07-27'')', TIMESTAMPADD(WEEK,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(WEEK,-1.6,''2022-07-27'')', TIMESTAMPADD(WEEK,-1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1.1,''2022-07-27'')', TIMESTAMPADD(DAY,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1.1,''2022-07-27'')', TIMESTAMPADD(DAY,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1.6,''2022-07-27'')', TIMESTAMPADD(DAY,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1.6,''2022-07-27'')', TIMESTAMPADD(DAY,-1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1.1,''2022-07-27'')', TIMESTAMPADD(HOUR,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1.1,''2022-07-27'')', TIMESTAMPADD(HOUR,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1.6,''2022-07-27'')', TIMESTAMPADD(HOUR,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1.6,''2022-07-27'')', TIMESTAMPADD(HOUR,-1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1.1,''2022-07-27'')', TIMESTAMPADD(MINUTE,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1.1,''2022-07-27'')', TIMESTAMPADD(MINUTE,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1.6,''2022-07-27'')', TIMESTAMPADD(MINUTE,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1.6,''2022-07-27'')', TIMESTAMPADD(MINUTE,-1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1.1,''2022-07-27'')', TIMESTAMPADD(SECOND,1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1.1,''2022-07-27'')', TIMESTAMPADD(SECOND,-1.1,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1.6,''2022-07-27'')', TIMESTAMPADD(SECOND,1.6,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1.6,''2022-07-27'')', TIMESTAMPADD(SECOND,-1.6,'2022-07-27'));

insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1,''2020-02-29'')', TIMESTAMPADD(YEAR,1,'2020-02-29'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1,''2020-02-29'')', TIMESTAMPADD(YEAR,-1,'2020-02-29'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1,''2022-08-31'')', TIMESTAMPADD(MONTH,1,'2022-08-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1,''2022-07-31'')', TIMESTAMPADD(MONTH,-1,'2022-07-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1,''2022-12-31'')', TIMESTAMPADD(MONTH,1,'2022-12-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1,''2022-01-31'')', TIMESTAMPADD(MONTH,-1,'2022-01-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''2022-01-01'')', TIMESTAMPADD(DAY,-1,'2022-01-01'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,49,''2022-10-30'')', TIMESTAMPADD(HOUR,49,'2022-10-30'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-56,''2022-07-01'')', TIMESTAMPADD(HOUR,-56,'2022-07-01'));

insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,''2022-07-27 23:30:00'')', TIMESTAMPADD(HOUR,1,'2022-07-27 23:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1,''2022-07-27 00:30:00'')', TIMESTAMPADD(HOUR,-1,'2022-07-27 00:30:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,1,''2022-07-27 08:59:59'')', TIMESTAMPADD(MINUTE,1,'2022-07-27 08:59:59'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,-1,''2022-07-27 08:00:00'')', TIMESTAMPADD(MINUTE,-1,'2022-07-27 08:00:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,1,''2022-07-27 08:30:59'')', TIMESTAMPADD(SECOND,1,'2022-07-27 08:30:59'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-1,''2022-07-27 00:00:00'')', TIMESTAMPADD(SECOND,-1,'2022-07-27 00:00:00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,0.001,''2022-07-27 08:30:59.999'')', TIMESTAMPADD(SECOND,0.001,'2022-07-27 08:30:59.999'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,-0.001,''2022-07-27 00:00:00'')', TIMESTAMPADD(SECOND,-0.001,'2022-07-27 00:00:00'));

--step3:插入入参为date格式但返回值为datetime格式的timestampadd用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,3,''2022-07-27'')', TIMESTAMPADD(HOUR,3,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,0.3,''2022-07-27'')', TIMESTAMPADD(HOUR,0.3,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,3,''2022-07-27'')', TIMESTAMPADD(MINUTE,3,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MINUTE,0.3,''2022-07-27'')', TIMESTAMPADD(MINUTE,0.3,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,3,''2022-07-27'')', TIMESTAMPADD(SECOND,3,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,0.03,''2022-07-27'')', TIMESTAMPADD(SECOND,0.03,'2022-07-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(SECOND,0.000000003,''2022-07-27'')', TIMESTAMPADD(SECOND,0.000000003,'2022-07-27'));

--step4:插入timestampadd涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,''9999-12-31'')', TIMESTAMPADD(DAY,1,'9999-12-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''0001-01-01'')', TIMESTAMPADD(DAY,-1,'0001-01-01'));

--step5:插入非法入参时timestampadd执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,1,''2022-07-36'')', TIMESTAMPADD(YEAR,1,'2022-07-36'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1,''2022-14-27'')', TIMESTAMPADD(YEAR,-1,'2022-14-27'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1,''2022-12-32'')', TIMESTAMPADD(MONTH,1,'2022-12-32'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-1,''2022-01-00'')', TIMESTAMPADD(MONTH,-1,'2022-01-00'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,1,''2022-02-29'')', TIMESTAMPADD(DAY,1,'2022-02-29'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1,''2022-14-32'')', TIMESTAMPADD(DAY,-1,'2022-14-32'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1,''2022-14-32'')', TIMESTAMPADD(HOUR,1,'2022-14-32'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-1,''2022-02-29'')', TIMESTAMPADD(HOUR,-1,'2022-02-29'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,10000000000,''9999999999-12-31'')', TIMESTAMPADD(YEAR,10000000000,'9999999999-12-31'));
insert into func_test(functionName, result) values('TIMESTAMPADD(YEAR,-1000000000,''999999999-99999-999999'')', TIMESTAMPADD(YEAR,-1000000000,'999999999-99999-999999'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,1000000000000000000000000000000000,''2022-12-28'')', TIMESTAMPADD(MONTH,1000000000000000000000000000000000,'2022-12-28'));
insert into func_test(functionName, result) values('TIMESTAMPADD(MONTH,-10000000000000000000000000000000,''2022-01-01'')', TIMESTAMPADD(MONTH,-10000000000000000000000000000000,'2022-01-01'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,99999999999999999,''2022-02-06'')', TIMESTAMPADD(DAY,99999999999999999,'2022-02-06'));
insert into func_test(functionName, result) values('TIMESTAMPADD(DAY,-1000000000000000000000000000000,''2022-06-07'')', TIMESTAMPADD(DAY,-1000000000000000000000000000000,'2022-06-07'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,1000000000000000000000000000000,''2022-11-21'')', TIMESTAMPADD(HOUR,1000000000000000000000000000000,'2022-11-21'));
insert into func_test(functionName, result) values('TIMESTAMPADD(HOUR,-10000000000000000000000000000,''2022-04-05'')', TIMESTAMPADD(HOUR,-10000000000000000000000000000,'2022-04-05'));

--step6:查看timestampadd函数执行结果是否正确;expect:成功
select * from func_test;

--step7:清理环境;expect:成功
drop table if exists func_test;