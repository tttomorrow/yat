--  @testpoint:opengauss关键字join(保留)，作为游标名

--前置条件
drop table if exists join_test cascade;
create table join_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor join for select * from join_test order by 1;
close join;
end;

--关键字带双引号-成功
start transaction;
cursor "join" for select * from join_test order by 1;
close "join";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'join' for select * from join_test order by 1;
close 'join';
end;

--关键字带反引号-合理报错
start transaction;
cursor `join` for select * from join_test order by 1;
close `join`;
end;

--清理环境
drop table join_test cascade;