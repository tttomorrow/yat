--  @testpoint:opengauss关键字Key_Member(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists Key_Member;
create group Key_Member with password 'Gauss@123';
drop group Key_Member;

--关键字带双引号-成功
drop group if exists "Key_Member";
create group "Key_Member" with password 'Gauss@123';
drop group "Key_Member";

--关键字带单引号-合理报错
drop group if exists 'Key_Member';
create group 'Key_Member' with password 'Gauss@123';

--关键字带反引号-合理报错
drop group if exists `Key_Member`;
create group `Key_Member` with password 'Gauss@123';
