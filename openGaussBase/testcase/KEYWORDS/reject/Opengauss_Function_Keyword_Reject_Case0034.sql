--  @testpoint:opengauss关键字reject(保留)，作为游标名

--前置条件
drop table if exists reject_test cascade;
create table reject_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor reject for select * from reject_test order by 1;
close reject;
end;

--关键字带双引号-成功
start transaction;
cursor "reject" for select * from reject_test order by 1;
close "reject";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'reject' for select * from reject_test order by 1;
close 'reject';
end;

--关键字带反引号-合理报错
start transaction;
cursor `reject` for select * from reject_test order by 1;
close `reject`;
end;

--清理环境
drop table reject_test cascade;