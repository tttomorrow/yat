-- @testpoint: gs_wlm_get_resource_pool_info(int),获取所有用户的资源使用统计信息，当入参为无效值（为空、字母、特殊字符、多参）时，合理报错

select gs_wlm_get_resource_pool_info();
select gs_wlm_get_resource_pool_info('a');
select gs_wlm_get_resource_pool_info('@#$');
select gs_wlm_get_resource_pool_info(1,2);