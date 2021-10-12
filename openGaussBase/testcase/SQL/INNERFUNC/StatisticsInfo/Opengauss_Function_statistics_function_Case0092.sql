-- @testpoint: gs_wlm_readjust_user_space_through_username(text name),修正指定用户的存储空间使用情况，当入参为无效值（为空、特殊字符、多参）时，合理报错

select gs_wlm_readjust_user_space_through_username();
select gs_wlm_readjust_user_space_through_username('@_123##');
select gs_wlm_readjust_user_space_through_username('yat','test');
select gs_wlm_readjust_user_space_through_username('yat_aaa');
