-- @testpoint: opengauss关键字like(保留)，作为用户组名 合理报错


--关键字不带引号-合理报错
drop group if exists like;
create group like with password 'haha@123';

--关键字带双引号-成功
drop group if exists "like";
create group "like" with password 'haha@123';

--清理环境
drop group "like";

--关键字带单引号-合理报错
drop group if exists 'like';
create group 'like' with password 'haha@123';

--关键字带反引号-合理报错
drop group if exists `like`;
create group `like` with password 'haha@123';
