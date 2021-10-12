-- @testpoint: opengauss关键字prior(非保留)，作为游标名,合理报错

--前置条件
drop table if exists prior_test cascade;
create table prior_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor prior for select * from prior_test order by 1;
close prior;
end;

--关键字带双引号-成功
start transaction;
cursor "prior" for select * from prior_test order by 1;
close "prior";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'prior' for select * from prior_test order by 1;
close 'prior';
end;

--关键字带反引号-合理报错
start transaction;
cursor `prior` for select * from prior_test order by 1;
close `prior`;
end;

--清理环境
drop table if exists prior_test cascade;