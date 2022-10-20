-- @testpoint: 时间函数timediff功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入timediff(datetime, time)参数格式且入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMEDIFF(''2007-12-31 23:59:59.999999'',''2007-12-01 1:1:1.000002'')', TIMEDIFF('2007-12-31 23:59:59.999999','2007-12-01 1:1:1.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2007-12-31 23:59:59.999999'',''2007-12-01 1:1:1.000002'')',TIMEDIFF('2007-12-31 23:59:59.999999','2007-12-01 1:1:1.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2007-12-31 0:0:0.999999'',''2007-12-30 1:1:1.000002'')', TIMEDIFF('2007-12-31 0:0:0.999999','2007-12-30 1:1:1.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-01-01 00:00:00'',''2000-01-01 00:00:00.000001'')', TIMEDIFF('2000-01-01 00:00:00','2000-01-01 00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-01-01 00:00:00'',''2000-01-02 00:00:00.000001'')', TIMEDIFF('2000-01-01 00:00:00','2000-01-02 00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-01-01 00:00:00'',''2000-02-01 00:00:00.000001'')', TIMEDIFF('2000-01-01 00:00:00','2000-02-01 00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-01-01 00:00:01'',''2000-01-01 00:00:00.999999'')', TIMEDIFF('2000-01-01 00:00:01','2000-01-01 00:00:00.999999'));
insert into func_test(functionName, result) values('TIMEDIFF(''01-01-01 00:00:00'',''01-01-01 00:00:00.000001'')', TIMEDIFF('01-01-01 00:00:00','01-01-01 00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:59:59.000001'',''2008-12-30 01:01:01.000002'')', TIMEDIFF('2008-12-31 23:59:59.000001','2008-12-30 01:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:59:59.0000015'',''2008-12-30 01:01:01.999999'')', TIMEDIFF('2008-12-31 23:59:59.0000015','2008-12-30 01:01:01.999999'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:59:59.0000014'',''2008-12-30 01:01:01.000002'')', TIMEDIFF('2008-12-31 23:59:59.0000014','2008-12-30 01:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:59:59.000001'',''2008-12-30 01:01:01.000002'')', TIMEDIFF('2008-12-31 23:59:59.000001','2008-12-30 01:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''1000-1-1 20:59:59'', ''1000-01-01 1:00'')', TIMEDIFF('1000-1-1 20:59:59', '1000-01-01 1:00') );

--step3:插入timediff(datetime, time)参数格式但涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMEDIFF(''2000-02-28 20:59:59'', ''2001-02-28 23:00'')', TIMEDIFF('2000-02-28 20:59:59', '2001-02-28 23:00') );
insert into func_test(functionName, result) values('TIMEDIFF(''0-01-01 00:00:00'',''2000-01-01 00:00:00.000001'')', TIMEDIFF('0-01-01 00:00:00','2000-01-01 00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''1-01-1 20:59:59'', ''2001-01-01 21:00'');', TIMEDIFF('1-01-1 20:59:59', '2001-01-01 21:00')   );
insert into func_test(functionName, result) values('TIMEDIFF(''10000-1-1 20:59:59'', ''2001-01-01 21:00'')', TIMEDIFF('10000-1-1 20:59:59', '2001-01-01 21:00') );

--step4:插入timediff(time, time)参数格式且入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMEDIFF(''-37:59:59'', ''-39:59:59'')', TIMEDIFF('-37:59:59', '-39:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''-37:59:59'', ''39:59:59'')', TIMEDIFF('-37:59:59', '39:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''37:59:59'', ''-39:59:59'')', TIMEDIFF('37:59:59', '-39:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''37:59:59'', ''39:59:59'')', TIMEDIFF('37:59:59', '39:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''01:00:00.999999'', ''02:00:00.999998'')', TIMEDIFF('01:00:00.999999', '02:00:00.999998'));
insert into func_test(functionName, result) values('TIMEDIFF(''24:00:00.999999'', ''02:00:00.999998'')', TIMEDIFF('24:00:00.999999', '02:00:00.999998'));
insert into func_test(functionName, result) values('TIMEDIFF(''01:00:00.000000'', ''02:00:00.999999'')', TIMEDIFF('01:00:00.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('TIMEDIFF(''60:00:00.000000'', ''02:00:00.999999'')', TIMEDIFF('60:00:00.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-01-01 00:00:00'',''2000-01-01 00:00:00.000001'')', TIMEDIFF('2000-01-01 00:00:00','2000-01-01 00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''00:00:00'',''00:00:00.000001'')', TIMEDIFF('00:00:00','00:00:00.000001'));
insert into func_test(functionName, result) values('TIMEDIFF(''-375959'', ''-395959'')', TIMEDIFF('-375959', '395959') );
insert into func_test(functionName, result) values('TIMEDIFF(''-375959.000002'', ''-395959.000001'')', TIMEDIFF('-375959.000002', '395959.000001') );
insert into func_test(functionName, result) values('TIMEDIFF(-375959, 395959)', TIMEDIFF(-375959, 395959) );  
insert into func_test(functionName, result) values('TIMEDIFF(-375959.000002, 395959.000001)', TIMEDIFF(-375959.000002, 395959.000001) );

--step5:插入timediff(time, time)参数格式但涉及时间类型值超出范围的的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMEDIFF(''838:59:59'', ''-25:00'')', TIMEDIFF('838:59:59', '-25:00') );
insert into func_test(functionName, result) values('TIMEDIFF(''-838:59:59'', ''25:00'')', TIMEDIFF('-838:59:59', '25:00') );
insert into func_test(functionName, result) values('TIMEDIFF(''839:59:59'', ''837:59:59'')', TIMEDIFF('839:59:59', '837:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''-837:59:59'', ''-839:59:59'')', TIMEDIFF('-837:59:59', '-839:59:59') );

--step6:插入入参为特殊类型的timediff用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMEDIFF(''2000-02-28 20:59:59'', NULL)', TIMEDIFF('2000-02-28 20:59:59', NULL) );
insert into func_test(functionName, result) values('TIMEDIFF(NULL, ''2000-02-28 20:59:59'')', TIMEDIFF(NULL, '2000-02-28 20:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(NULL, ''-839:59:59'')', TIMEDIFF(NULL, '-839:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''-837:59:59'', NULL)', TIMEDIFF('-837:59:59', NULL) );
insert into func_test(functionName, result) values('TIMEDIFF(false, true)', TIMEDIFF(false, true) );
insert into func_test(functionName, result) values('TIMEDIFF(B''101'', B''101'')', TIMEDIFF(B'101', B'101') );
insert into func_test(functionName, result) values('TIMEDIFF(cast(''2000-02-28 20:59:59'' as datetime), cast(''2000-02-28 23:00'' as datetime))', TIMEDIFF(cast('2000-02-28 20:59:59' as datetime), cast('2000-02-28 23:00' as datetime)));
insert into func_test(functionName, result) values('TIMEDIFF(cast(''2008-12-31 23:59:59.000001'' as datetime), time''22:01:01.000002'')', TIMEDIFF(cast('2008-12-31 23:59:59.000001' as datetime), time'22:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(cast(''2008-12-31 23:59:59.000001'' as datetime), date''2008-12-30'')', TIMEDIFF(cast('2008-12-31 23:59:59.000001' as datetime), date'2008-12-30'));
insert into func_test(functionName, result) values('TIMEDIFF(time''23:59:59.000001'', cast(''2008-12-30 22:01:01.000002'' as datetime)))', TIMEDIFF(time'23:59:59.000001', cast('2008-12-30 22:01:01.000002' as datetime)));
insert into func_test(functionName, result) values('TIMEDIFF(time''23:59:59.000001'', date''2008-12-30'')', TIMEDIFF(time'23:59:59.000001', date'2008-12-30'));
insert into func_test(functionName, result) values('TIMEDIFF(time''-37:59:59'', time''-39:59:59'')', TIMEDIFF(time'-37:59:59', time'-39:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(date''2008-12-31'', cast(''2008-12-30 01:01:01.000002'' as datetime)))', TIMEDIFF(date'2008-12-31', cast('2008-12-30 01:01:01.000002' as datetime)));
insert into func_test(functionName, result) values('TIMEDIFF(date''2008-12-31'', date''2008-12-30'')', TIMEDIFF(date'2008-12-31', date'2008-12-30'));
insert into func_test(functionName, result) values('TIMEDIFF(date''2008-12-31'', time''22:01:01.000002'')', TIMEDIFF(date'2008-12-31', time'22:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-02-28 20:59:59'', ''4:00'')', TIMEDIFF('2000-02-28 20:59:59', '4:00') );
insert into func_test(functionName, result) values('TIMEDIFF(''20:59:59'', ''2000-02-28 23:00'')', TIMEDIFF('2000-02-28 20:59:59', '2000-02-28 23:00') );

--step7:插入非法入参时timediff执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMEDIFF(''abcd'', ''-2000-02-28 20:59:59'')', TIMEDIFF('abcd', '-2000-02-28 20:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''2000-02-28 20:59:59'', ''abcd'')', TIMEDIFF('2000-02-28 20:59:59', 'abcd') );
insert into func_test(functionName, result) values('TIMEDIFF(''2007-12-40 23:59:59.999999'',''2000-02-28 20:59:59'')', TIMEDIFF('2007-12-40 23:59:59.999999','2000-02-28 20:59:59'));
insert into func_test(functionName, result) values('TIMEDIFF(''2007-13-31 23:59:59.999999'',''2000-02-28 20:59:59'')', TIMEDIFF('2007-13-31 23:59:59.999999','2000-02-28 20:59:59'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 24:59:59.000001'',''2008-12-30 01:01:01.000002'')', TIMEDIFF('2008-12-31 24:59:59.000001','2008-12-30 01:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:60:59.000001'',''2008-12-30 01:01:01.000002'')', TIMEDIFF('2008-12-31 23:60:59.000001','2008-12-30 01:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:59:59.000001'',''2008-12-30 01:60:01.000002'')', TIMEDIFF('2008-12-31 23:59:59.000001','2008-12-30 01:60:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2008-12-31 23:59:59.000001'',''2008-12-30 24:01:01.000002'')', TIMEDIFF('2008-12-31 23:59:59.000001','2008-12-30 24:01:01.000002'));
insert into func_test(functionName, result) values('TIMEDIFF(''2000-13-01 00:00:00'',''2000-01-01 00:00:00.000001'')', TIMEDIFF('2000-13-01 00:00:00','2000-01-01 00:00:00.000001'));

insert into func_test(functionName, result) values('TIMEDIFF(''abcd'', ''-839:59:59'')', TIMEDIFF('abcd', '-839:59:59') );
insert into func_test(functionName, result) values('TIMEDIFF(''-837:59:59'', ''abcd'')', TIMEDIFF('-837:59:59', 'abcd') );
insert into func_test(functionName, result) values('TIMEDIFF(''02:00:61.000000'', ''02:00:00.999999'')', TIMEDIFF('02:00:61.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('TIMEDIFF(''02:61:00.000000'', ''02:00:00.999999'')', TIMEDIFF('02:61:00.000000', '02:00:00.999999'));

insert into func_test(functionName, result) values('TIMEDIFF(''2000-01-01'', ''2022-01-01'')', TIMEDIFF('2000-01-01', '2022-01-01') );

--step8:查看timediff函数执行结果是否正确;expect:成功
select * from func_test;

--step9:清理环境;expect:成功
drop table if exists func_test;