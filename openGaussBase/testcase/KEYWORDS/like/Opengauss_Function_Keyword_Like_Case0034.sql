-- @testpoint: opengauss关键字like(保留)，作为游标名 合理报错

--前置条件
drop table if exists like_test cascade;
create table like_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor like for select * from like_test order by 1;
close like;
end;

--关键字带双引号-成功
start transaction;
cursor "like" for select * from like_test order by 1;
close "like";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'like' for select * from like_test order by 1;
close 'like';
end;

--关键字带反引号-合理报错
start transaction;
cursor `like` for select * from like_test order by 1;
close `like`;
end;

--清理环境
drop table like_test cascade;