-- @testpoint: 时间函数sec_to_time功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入sec_to_time执行结果;expect:成功
insert into func_test(functionName, result) values ('sec_to_time(''1000'')', sec_to_time('1000'));
insert into func_test(functionName, result) values ('sec_to_time(''1000.5'')', sec_to_time('1000.5'));
insert into func_test(functionName, result) values ('sec_to_time(1000.5)', sec_to_time(1000.5));
insert into func_test(functionName, result) values ('sec_to_time(''abcd'')', sec_to_time('abcd'));
insert into func_test(functionName, result) values ('sec_to_time(true)', sec_to_time(true));
insert into func_test(functionName, result) values ('sec_to_time(B''1111'')', sec_to_time(B'1111'));
insert into func_test(functionName, result) values ('sec_to_time(NULL)', sec_to_time(NULL));
insert into func_test(functionName, result) values ('sec_to_time(pow(10,18))', sec_to_time(pow(10,18)));
insert into func_test(functionName, result) values ('sec_to_time(pow(10,18)-1)', sec_to_time(pow(10,18)-1));
insert into func_test(functionName, result) values ('sec_to_time(1000)', sec_to_time(1000));
insert into func_test(functionName, result) values ('sec_to_time(0)', sec_to_time(0));
insert into func_test(functionName, result) values ('sec_to_time(-1000000)', sec_to_time(-1000000));
insert into func_test(functionName, result) values ('sec_to_time(1000000.499)', sec_to_time(1000000.499));
insert into func_test(functionName, result) values ('sec_to_time(1000000.4990000)', sec_to_time(1000000.4990000));
insert into func_test(functionName, result) values ('sec_to_time(1000000.4999994999)', sec_to_time(1000000.4999994999));
insert into func_test(functionName, result) values ('sec_to_time(1000000.499999500)', sec_to_time(1000000.499999500));
insert into func_test(functionName, result) values ('sec_to_time(1000000.499998500)', sec_to_time(1000000.499998500));
insert into func_test(functionName, result) values ('sec_to_time(0.999999500)', sec_to_time(0.999999500));
insert into func_test(functionName, result) values ('sec_to_time(59.999999600)', sec_to_time(59.999999600));
insert into func_test(functionName, result) values ('sec_to_time(3599.999999700)', sec_to_time(3599.999999700));
insert into func_test(functionName, result) values ('sec_to_time(3020399)', sec_to_time(3020399));
insert into func_test(functionName, result) values ('sec_to_time(3020399 + 1)', sec_to_time(3020399 + 1));
insert into func_test(functionName, result) values ('sec_to_time(3020399.000000500)', sec_to_time(3020399.000000500));

--step3:查看sec_to_time函数执行结果是否正确;expect:成功
select * from func_test;

--step4:清理环境;expect:成功
drop table if exists func_test;