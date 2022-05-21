-- @testpoint: opengauss关键字nvarchar(非保留)，作为用户组名 部分测试点合理报错


--step1:关键字不带引号-成功
drop group if exists nvarchar;
create group nvarchar with password 'gauss@123';
drop group nvarchar;

--step2:关键字带双引号-成功
drop group if exists "nvarchar";
create group "nvarchar" with password 'gauss@123';
drop group "nvarchar";

--step3:关键字带单引号-合理报错
drop group if exists 'nvarchar';
create group 'nvarchar' with password 'gauss@123';

--step4:关键字带反引号-合理报错
drop group if exists `nvarchar`;
create group `nvarchar` with password 'gauss@123';
