-- @testpoint: gs_wlm_session_respool(bigint)获取当前所有后台线程的session resouce pool相关信息,当入参为无效值（为空、字母、特殊字符、多参）时，合理报错

select gs_wlm_session_respool();
select gs_wlm_session_respool('a');
select gs_wlm_session_respool('@#$');
select gs_wlm_session_respool(1,2);
