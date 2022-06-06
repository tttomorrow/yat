-- @testpoint: gs_wlm_user_resource_info(name text),查询具体某个用户的资源限额和资源使用情况,入参为无效值（为空、特殊字符、多参）时，合理报错

select gs_wlm_user_resource_info();
select gs_wlm_user_resource_info('@#$');
select gs_wlm_user_resource_info(1,2);
