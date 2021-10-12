--  @testpoint:opengauss关键字returned_length(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists returned_length;
create group returned_length with password 'gauss@123';
drop group returned_length;

--关键字带双引号-成功
drop group if exists "returned_length";
create group "returned_length" with password 'gauss@123';
drop group "returned_length";

--关键字带单引号-合理报错
drop group if exists 'returned_length';

--关键字带反引号-合理报错
drop group if exists `returned_length`;

