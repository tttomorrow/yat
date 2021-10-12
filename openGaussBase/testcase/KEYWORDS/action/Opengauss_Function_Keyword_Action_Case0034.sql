--  @testpoint:opengauss关键字action(非保留)，作为游标名
--前置条件
drop table if exists action_test cascade;
create table action_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor action for select * from action_test order by 1;
close action;
end;

--关键字带双引号-成功
start transaction;
cursor "action" for select * from action_test order by 1;
close "action";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'action' for select * from action_test order by 1;
close 'action';
end;

--关键字带反引号-合理报错
start transaction;
cursor `action` for select * from action_test order by 1;
close `action`;
end;

--清理环境
drop table action_test;