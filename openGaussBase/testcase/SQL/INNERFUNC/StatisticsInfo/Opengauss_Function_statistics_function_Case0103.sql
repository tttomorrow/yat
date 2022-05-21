-- @testpoint: fenced_udf_process(int)描述：查看本地udf master和work进程数,入参为有效值

----step1：入参为有效值; expect:成功
select fenced_udf_process(1);
select fenced_udf_process(2);
select fenced_udf_process(3);