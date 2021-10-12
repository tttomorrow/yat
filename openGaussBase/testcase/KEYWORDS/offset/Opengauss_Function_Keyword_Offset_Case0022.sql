--  @testpoint:opengauss关键字offset(保留)，作为用户组名


--关键字不带引号-合理报错
drop group if exists offset;
create group offset with password 'gauss@123';

--关键字带双引号-成功
drop group if exists "offset";
create group "offset" with password 'gauss@123';

--清理环境
drop group "offset";

--关键字带单引号-合理报错
drop group if exists 'offset';
create group 'offset' with password 'gauss@123';

--关键字带反引号-合理报错
drop group if exists `offset`;
create group `offset` with password 'gauss@123';
