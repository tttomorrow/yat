--  @testpoint:opengauss关键字revoke(非保留)，作为游标名
--前置条件
drop table if exists revoke_test cascade;
create table revoke_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor revoke for select * from revoke_test order by 1;
close revoke;
end;

--关键字带双引号-成功
start transaction;
cursor "revoke" for select * from revoke_test order by 1;
close "revoke";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'revoke' for select * from revoke_test order by 1;
close 'revoke';
end;

--关键字带反引号-合理报错
start transaction;
cursor `revoke` for select * from revoke_test order by 1;
close `revoke`;
end;

--清理环境
drop table revoke_test;