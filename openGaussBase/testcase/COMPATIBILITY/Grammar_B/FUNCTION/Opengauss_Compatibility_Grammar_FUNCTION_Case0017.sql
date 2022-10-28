-- @testpoint: 时间函数unix_timestamp功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时unix_timestamp执行结果;expect:成功
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-27'')', UNIX_TIMESTAMP('2022-07-27'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''20220727'')', UNIX_TIMESTAMP('20220727'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-27 15:25:30'')', UNIX_TIMESTAMP('2022-07-27 15:25:30'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''20220727152530'')', UNIX_TIMESTAMP('20220727152530'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-27 15:25:30.8888855'')', UNIX_TIMESTAMP('2022-07-27 15:25:30.8888855'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''20220727152530.8888854'')', UNIX_TIMESTAMP('20220727152530.8888854'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(050505)', UNIX_TIMESTAMP(050505));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(20220801)', UNIX_TIMESTAMP(20220801));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(20220801182030)', UNIX_TIMESTAMP(20220801182030));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(20220801182030.8888855)', UNIX_TIMESTAMP(20220801182030.8888855));

--step3:插入入参为特殊类型的unix_timestamp用例执行结果;expect:成功
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(null)', UNIX_TIMESTAMP(null));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(date''2022-04-05'')', UNIX_TIMESTAMP(date'2022-04-05'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(cast(''2022-04-05 14:35:00'' as datetime))', UNIX_TIMESTAMP(cast('2022-04-05 14:35:00' as datetime)));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(cast(''2022-04-05 14:35:00.888'' as datetime))', UNIX_TIMESTAMP(cast('2022-04-05 14:35:00.888' as datetime)));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(time''1:1:1'')', UNIX_TIMESTAMP(time'1:1:1'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(time''25:00:00'')', UNIX_TIMESTAMP(time'25:00:00'));

--step4:插入非法入参时unix_timestamp用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(true)', UNIX_TIMESTAMP(true));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-32'')', UNIX_TIMESTAMP('2022-07-32'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-13-27'')', UNIX_TIMESTAMP('2022-13-27'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-27 12:00:61'')', UNIX_TIMESTAMP('2022-07-27 12:00:61'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-27 12:61:00'')', UNIX_TIMESTAMP('2022-07-27 12:61:00'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2022-07-27 25:00:00'')', UNIX_TIMESTAMP('2022-07-27 25:00:00'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''99999999999999999999-07-27'')', UNIX_TIMESTAMP('99999999999999999999-07-27'));

--step5:插入unix_timestamp返回结果超出指定范围的用例执行结果;expect:成功
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2038-01-19'')', UNIX_TIMESTAMP('2038-01-19'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2038-01-19 11:14:07'')', UNIX_TIMESTAMP('2038-01-19 11:14:07'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2038-01-19 11:14:07.9999'')', UNIX_TIMESTAMP('2038-01-19 11:14:07.9999'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2038-01-19 11:14:07.999999999'')', UNIX_TIMESTAMP('2038-01-19 11:14:07.999999999'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''2038-01-19 11:14:08'')', UNIX_TIMESTAMP('2038-01-19 11:14:08'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''1970-01-01'')', UNIX_TIMESTAMP('1970-01-01'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''1970-01-01 08:00:00'')', UNIX_TIMESTAMP('1970-01-01 08:00:00'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''1970-01-01 08:00:01'')', UNIX_TIMESTAMP('1970-01-01 08:00:01'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''1970-01-01 08:00:00.999999'')', UNIX_TIMESTAMP('1970-01-01 08:00:00.999999'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''1970-01-01 07:59:59'')', UNIX_TIMESTAMP('1970-01-01 07:59:59'));
insert into func_test(functionName, result) values('UNIX_TIMESTAMP(''1969-12-31'')', UNIX_TIMESTAMP('1969-12-31'));

--step6: og时间类型与格式测试;expect:部分类型合理报错
insert into func_test(functionName, result) values('unix_timestamp(timetz''1:0:0+05'')', unix_timestamp(timetz'1:0:0+05'));
insert into func_test(functionName, result) values('unix_timestamp(timestamptz''2000-1-1 1:1:1+05'')', unix_timestamp(timestamptz'2000-1-1 1:1:1+05'));
insert into func_test(functionName, result) values('unix_timestamp(reltime''2000 years 1 mons 1 days 1:1:1'')', unix_timestamp(reltime'2000 years 1 mons 1 days 1:1:1'));
insert into func_test(functionName, result) values('unix_timestamp(abstime''2000-1-1 1:1:1+05'')', unix_timestamp(abstime'2000-1-1 1:1:1+05'));
insert into func_test(functionName, result) values('unix_timestamp(''23:0:0+05'')', unix_timestamp('23:0:0+05'));
insert into func_test(functionName, result) values('unix_timestamp(''2000 years 1 mons 1 days 1:1:1'')', unix_timestamp('2000 years 1 mons 1 days 1:1:1'));
insert into func_test(functionName, result) values('unix_timestamp(''2000-1-1 23:1:1+05'')', unix_timestamp('2000-1-1 23:1:1+05'));

--step7: og时间边界测试;expect:部分用例合理报错
insert into func_test(functionName, result) values('unix_timestamp(date''4714-11-24bc'')', unix_timestamp(date'4714-11-24bc'));
insert into func_test(functionName, result) values('unix_timestamp(date''5874897-12-31'')', unix_timestamp(date'5874897-12-31'));
insert into func_test(functionName, result) values('unix_timestamp(datetime''4714-11-24 00:00:00 bc'')', unix_timestamp(datetime'4714-11-24 00:00:00 bc'));
insert into func_test(functionName, result) values('unix_timestamp(datetime''294277-1-9 4:00:54.775807'')', unix_timestamp(datetime'294277-1-9 4:00:54.775807'));
insert into func_test(functionName, result) values('unix_timestamp(datetime''294277-1-9 4:00:54.775806'')', unix_timestamp(datetime'294277-1-9 4:00:54.775806'));

--step8:查看unix_timestamp函数执行结果是否正确;expect:成功
select * from func_test;

--step9:清理环境;expect:成功
drop table if exists func_test;