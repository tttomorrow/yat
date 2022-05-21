-- @testpoint: fenced_udf_process(int)描述：查看本地udf master和work进程数,入参为无效值（为空、特殊字符、多参）时，合理报错

----step1：入参为空; expect:合理报错
select fenced_udf_process();

----step2：入参为特殊字符; expect:合理报
select fenced_udf_process('@&*');

----step3：多参; expect:合理报错
select fenced_udf_process(1,2);