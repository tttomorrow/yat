-- @testpoint: gs_wlm_readjust_user_space_with_reset_flag(text name, boolean isfirst)，修正指定用户的存储空间使用情况，当入参为无效值（为空、特殊字符、多参、用户不存在）时，合理报错

----step1：入参为空; expect:合理报错
select gs_wlm_readjust_user_space_with_reset_flag();

----step2：入参为特殊字符; expect:合理报
select gs_wlm_readjust_user_space_with_reset_flag('@_##',true);

----step3：多参; expect:合理报
select gs_wlm_readjust_user_space_with_reset_flag('yat','test',true);

----step4：用户不存在; expect:合理报
select gs_wlm_readjust_user_space_with_reset_flag('yat_aaa',true);