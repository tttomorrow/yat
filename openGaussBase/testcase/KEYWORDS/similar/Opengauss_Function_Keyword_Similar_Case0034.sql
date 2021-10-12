-- @testpoint: opengauss关键字similar(保留)，作为游标名，合理报错

--前置条件
drop table if exists similar_test cascade;
create table similar_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor similar for select * from similar_test order by 1;
close similar;
end;

--关键字带双引号-成功
start transaction;
cursor "similar" for select * from similar_test order by 1;
close "similar";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'similar' for select * from similar_test order by 1;
close 'similar';
end;

--关键字带反引号-合理报错
start transaction;
cursor `similar` for select * from similar_test order by 1;
close `similar`;
end;

--清理环境
drop table similar_test cascade;