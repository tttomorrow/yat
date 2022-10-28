-- @testpoint: 时间函数subdate功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
drop table if exists insert_subdate;
create table func_test(functionName varchar(256),result varchar(256));
create table insert_subdate(date_col date, datetime_col datetime);

--step2:插入合法入参时subdate执行结果;expect:成功
insert into func_test(functionName, result) values ('subdate(''2022-1-1'', 20)',subdate('2022-1-1', '20'));
insert into func_test(functionName, result) values ('subdate(''2022-1-1'', ''20.5'')',subdate('2022-1-1', '20.5'));
insert into func_test(functionName, result) values ('subdate(''2022-1-1'', 20.5)',subdate('2022-1-1', 20.5));
insert into func_test(functionName, result) values ('subdate(''2022-1-1'', true)',subdate('2022-1-1', true));
insert into func_test(functionName, result) values ('subdate(''2022-1-1'', B''1111'')',subdate('2022-1-1', B'1111'));
insert into func_test(functionName, result) values ('subdate(date''2022-1-1'', 1)',subdate(date'2022-1-1', 1));
insert into func_test(functionName, result) values ('subdate(cast(''2022-1-1 1:1:1'' as datetime), 1)',subdate(cast('2022-1-1 1:1:1' as datetime), 1));
insert into func_test(functionName, result) values ('subdate(NULL, 20)',subdate(NULL, 20));
insert into func_test(functionName, result) values ('subdate(''2022-1-1'', NULL)',subdate('2022-1-1', NULL));
insert into func_test(functionName, result) values ('subdate(''2022-1-1 6:05:05'', INTERVAL ''10 20:20'' DAY TO SECOND)',subdate('2022-1-1 6:05:05', INTERVAL '10 20:20' DAY TO SECOND));
insert into func_test(functionName, result) values ('subdate(20220101010101.555, 1)',subdate(20220101010101.555, 1));
insert into func_test(functionName, result) values ('subdate(20220101, 1)',subdate(20220101, 1));
insert into func_test(functionName, result) values ('subdate(''2022-1-1 6:05:05'', INTERVAL ''6'' SECOND)',subdate('2022-1-1 6:05:05', INTERVAL '-6' SECOND));
insert into func_test(functionName, result) values ('subdate(''2022-6-1 6:05:05.5555555'', INTERVAL 6.444444 SECOND)',subdate('2022-6-1 6:05:05.5555555', INTERVAL 6.444444 SECOND));
insert into func_test(functionName, result) values ('subdate(''2022-6-1 6:05:05.444444'', INTERVAL ''6.555555'' HOUR TO SECOND)',subdate('2022-6-1 6:05:05.444444', INTERVAL '1:1:6.555555' HOUR TO SECOND));
insert into func_test(functionName, result) values ('subdate(''0001-1-1 00:00:01'', INTERVAL 1 SECOND)', subdate('0001-1-1 00:00:01', INTERVAL 1 SECOND));
insert into func_test(functionName, result) values ('subdate(''2020-2-28 23:59:59'', INTERVAL ''-1:1'' MINUTE TO SECOND)',subdate('2020-2-28 23:59:59', INTERVAL '-1:1' MINUTE TO SECOND));
insert into func_test(functionName, result) values ('subdate(''2020-2-29'', INTERVAL ''366'' DAY)',subdate('2020-2-29', INTERVAL '366' DAY));
insert into func_test(functionName, result) values ('subdate(''2020-2-29'', INTERVAL ''-366'' DAY)',subdate('2020-2-29', INTERVAL '-366' DAY));
insert into func_test(functionName, result) values ('subdate(''0001-1-2 1:1:1'', INTERVAL ''1'' DAY)',subdate('0001-1-2 1:1:1', INTERVAL '1' DAY));
insert into func_test(functionName, result) values ('subdate(''2020-2-29'', INTERVAL ''-365'' MONTH)',subdate('2020-2-29', INTERVAL '-365' MONTH));
insert into func_test(functionName, result) values ('subdate(''0001-1-31'', INTERVAL ''1'' MONTH)',subdate('0001-1-31', INTERVAL '1' MONTH));
insert into func_test(functionName, result) values ('subdate(''0001-2-1'', INTERVAL ''1'' MONTH)',subdate('0001-2-1', INTERVAL '1' MONTH));
insert into func_test(functionName, result) values ('subdate(''2020-2-29'', INTERVAL 3 YEAR)',subdate('2020-2-29', INTERVAL '3' YEAR));
insert into func_test(functionName, result) values ('subdate(''2020-2-29'', INTERVAL -3 YEAR)',subdate('2020-2-29', INTERVAL '-3' YEAR));
insert into func_test(functionName, result) values ('subdate(''0001-12-31'', INTERVAL ''1'' YEAR)',subdate('0001-12-31', INTERVAL '1' YEAR));
insert into func_test(functionName, result) values ('subdate(time''100:59:59'', INTERVAL ''1 20:50:50.888888'' DAY To SECOND)',subdate(time'100:59:59', INTERVAL '1 20:50:50.888888' DAY TO SECOND));
insert into func_test(functionName, result) values ('subdate(time''100:59:59'', INTERVAL ''-1 20:50:50.888888'' HOUR To SECOND)',subdate(time'100:59:59', INTERVAL '-20:50:50.888888' HOUR TO SECOND));
insert into func_test(functionName, result) values ('subdate(time(6)''100:59:59.555'', 2',subdate(time(6)'100:59:59.555', 2));

--step3:插入非法入参时subdate执行结果;expect:合理报错
insert into func_test(functionName, result) values ('subdate(''abcd'', ''abcd'')',subdate('abcd', 'abcd'));
insert into func_test(functionName, result) values ('subdate(''-0001-1-1'', INTERVAL ''6'' SECOND)', subdate('-0001-1-1', INTERVAL '6' SECOND));
insert into func_test(functionName, result) values ('subdate(''2022-11-30 25:00:00'', 20)',subdate('2022-11-30 25:00:00', 20));
insert into func_test(functionName, result) values ('subdate(''2022-11-30 00:60:00", 20)',subdate('2022-11-30 00:60:00', 20));
insert into func_test(functionName, result) values ('subdate(''2022-11-30 00:00:60'', 20)',subdate('2022-11-30 00:00:60', 20));
insert into func_test(functionName, result) values ('subdate(''2022-2-29'', INTERVAL ''6'' SECOND)',subdate('2022-2-29', INTERVAL '6' SECOND));
insert into func_test(functionName, result) values ('subdate(''2022-4-31'', 20)',subdate('2022-4-31', 20));
insert into func_test(functionName, result) values ('subdate("2022-0-1 6:05:05", 20)',subdate('2022-0-1 6:05:05', 20));
insert into func_test(functionName, result) values ('subdate("2022-1-0 6:05:05", INTERVAL ''6'' SECOND)',subdate('2022-1-0 6:05:05', INTERVAL '6' SECOND));

--step4:插入subdate返回时间类型结果超出范围执行结果;expect:合理报错
insert into func_test(functionName, result) values ('subdate(''10000-1-1'', INTERVAL ''6'' SECOND)', subdate('10000-1-1', INTERVAL '6' SECOND));
insert into func_test(functionName, result) values ('subdate(''0001-1-1 00:00:01.555555'', INTERVAL ''1.555556'' SECOND)',subdate('0001-1-1 00:00:01.555555', INTERVAL '1.555556' SECOND));
insert into func_test(functionName, result) values ('subdate(''9999-12-1 22:01:01.111111'', INTERVAL ''-30 1:58:58.888889'' DAY TO SECOND)',subdate('9999-12-1 22:01:01.111111', INTERVAL '-30 1:58:58.888889' DAY TO SECOND));
insert into func_test(functionName, result) values ('subdate(''0001-1-1 22:01:01'', INTERVAL ''366 22:01:02'' DAY TO SECOND)',subdate('0001-1-1 22:01:01', INTERVAL '366 22:01:02' DAY TO SECOND));
insert into func_test(functionName, result) values ('subdate(''0001-1-1 1:1:1'', INTERVAL ''1'' DAY)',subdate('0001-1-1 1:1:1', INTERVAL '1' DAY));
insert into func_test(functionName, result) values ('subdate(''9999-12-1'', -31)',subdate('9999-12-1', -31));
insert into func_test(functionName, result) values ('subdate(''0001-1-1'', 367)',subdate('0001-1-1', 367));
insert into func_test(functionName, result) values ('subdate(''9999-12-1'', INTERVAL ''-1'' MONTH)',subdate('9999-12-1', INTERVAL '-1' MONTH));
insert into func_test(functionName, result) values ('subdate(''0001-1-31'', INTERVAL ''13'' MONTH)',subdate('0001-1-31', INTERVAL '13' MONTH));
insert into func_test(functionName, result) values ('subdate(''9999-1-1'', INTERVAL ''-1'' YEAR)',subdate('9999-1-1', INTERVAL '-1' YEAR));
insert into func_test(functionName, result) values ('subdate(''2020-1-1'', INTERVAL ''2021'' YEAR)',subdate('2020-1-1', INTERVAL '2021' YEAR));
insert into func_test(functionName, result) values ('subdate(time''22:11:11'', INTERVAL ''1'' YEAR)',subdate(time'22:11:11', INTERVAL '1' YEAR));
insert into func_test(functionName, result) values ('subdate(time''22:11:11'', INTERVAL ''-1'' MONTH)',subdate(time'22:11:11', INTERVAL '-1' MONTH));
insert into func_test(functionName, result) values ('subdate(time''815:0:0'', -1)',subdate(time'815:0:0', -1));
insert into func_test(functionName, result) values ('subdate(time''-838:59:59'', INTERVAL ''1'' SECOND)',subdate(time'-838:59:59', INTERVAL '1' SECOND));

--step5:测试subdate返回结果能否正确插入表中;expect:成功
insert into insert_subdate(date_col, datetime_col) values (subdate('2021-1-1', 1), subdate('2021-1-1 01:01:01', 1));


--step6: og时间类型与格式测试;expect:部分类型合理报错
insert into func_test(functionName, result) values('subdate(timetz''1:0:0+05'', 1)', subdate(timetz'1:0:0+05', 1));
insert into func_test(functionName, result) values('subdate(timestamptz''2000-1-1 1:1:1+05'', 1)', subdate(timestamptz'2000-1-1 1:1:1+05', 1));
insert into func_test(functionName, result) values('subdate(reltime''2000 years 1 mons 1 days 1:1:1'', 1)', subdate(reltime'2000 years 1 mons 1 days 1:1:1', 1));
insert into func_test(functionName, result) values('subdate(abstime''2000-1-1 1:1:1+05'', 1)', subdate(abstime'2000-1-1 1:1:1+05', 1));
insert into func_test(functionName, result) values('subdate(''2000 years 1 mons 1 days 1:1:1'', 1)', subdate('2000 years 1 mons 1 days 1:1:1', 1));
insert into func_test(functionName, result) values('subdate(''2000-1-1 23:1:1+05'', 1)', subdate('2000-1-1 23:1:1+05', 1));

--step7: og时间边界测试;expect:合理报错
insert into func_test(functionName, result) values('subdate(datetime''4714-11-24 00:00:00 bc'', 1)', subdate(datetime'4714-11-24 00:00:00 bc', 1));
insert into func_test(functionName, result) values('subdate(datetime''294277-1-9 4:00:54.775807'', 1)', subdate(datetime'294277-1-9 4:00:54.775807', 1));
insert into func_test(functionName, result) values('subdate(datetime''294277-1-9 4:00:54.775806'', 1)', subdate(datetime'294277-1-9 4:00:54.775806', 1));
insert into func_test(functionName, result) values('subdate(date''4714-11-24bc'', 1)', subdate(date'4714-11-24bc', 1));
insert into func_test(functionName, result) values('subdate(date''5874897-12-31'', 1)', subdate(date'5874897-12-31', 1));

--step8:查看makedate函数执行结果是否正确;expect:成功
select * from func_test;

--step9:清理环境;expect:成功
drop table if exists insert_subdate;
drop table if exists func_test;