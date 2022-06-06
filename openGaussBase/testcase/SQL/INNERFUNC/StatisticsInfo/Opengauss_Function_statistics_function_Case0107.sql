-- @testpoint: reset_unique_sql(text, text, bigint),入参为无效值（为空、特殊字符、多参、少参、null）时，合理报错

----step1：入参为空; expect:合理报错
select reset_unique_sql();

----step2：入参为特殊字符; expect:合理报
select reset_unique_sql('#','@','1');

----step3：多参; expect:合理报错
select reset_unique_sql('global','all',2,1);

----step4：少参; expect:合理报错
select reset_unique_sql('global','all',);

----step5：入参有null值; expect:合理报错
select reset_unique_sql('global','all','null');
