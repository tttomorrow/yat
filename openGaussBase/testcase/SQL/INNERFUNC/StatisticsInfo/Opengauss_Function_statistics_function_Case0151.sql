-- @testpoint: create_wlm_operator_info(int flag),将当前内存中记录的TopSQL算子级别相关统计信息清理,当入参未无效值（为空、特殊字符、多参）时，合理报错

----step1：入参为空; expect:合理报错
select create_wlm_operator_info();

----step2：入参为特殊字符; expect:合理报错
select create_wlm_operator_info('@#$');

----step3：多参; expect:合理报错
select create_wlm_operator_info(1,2);


