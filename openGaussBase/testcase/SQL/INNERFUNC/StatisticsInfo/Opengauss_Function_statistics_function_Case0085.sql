-- @testpoint: gs_wlm_get_user_info(int),获取所有用户的相关信息，当入参为无效值（为空、字母、特殊字符、多参）时，合理报错

select gs_wlm_get_user_info();
select gs_wlm_get_user_info('a');
select gs_wlm_get_user_info('@#$');
select gs_wlm_get_user_info(1,2);