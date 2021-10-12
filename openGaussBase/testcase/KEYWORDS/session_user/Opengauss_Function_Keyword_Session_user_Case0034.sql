--  @testpoint:opengauss关键字session_user(保留)，作为游标名

--前置条件
drop table if exists session_user_test cascade;
create table session_user_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor session_user for select * from session_user_test order by 1;
close session_user;
end;

--关键字带双引号-成功
start transaction;
cursor "session_user" for select * from session_user_test order by 1;
close "session_user";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'session_user' for select * from session_user_test order by 1;
close 'session_user';
end;

--关键字带反引号-合理报错
start transaction;
cursor `session_user` for select * from session_user_test order by 1;
close `session_user`;
end;

--清理环境
drop table session_user_test cascade;