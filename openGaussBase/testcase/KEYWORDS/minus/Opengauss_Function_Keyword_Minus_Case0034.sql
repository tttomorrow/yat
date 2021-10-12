-- @testpoint: opengauss关键字minus(保留)，作为游标名,部分测试点合理报错

--前置条件
drop table if exists minus_test cascade;
create table minus_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor minus for select * from minus_test order by 1;
close minus;
end;

--关键字带双引号-成功
start transaction;
cursor "minus" for select * from minus_test order by 1;
close "minus";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'minus' for select * from minus_test order by 1;
close 'minus';
end;

--关键字带反引号-合理报错
start transaction;
cursor `minus` for select * from minus_test order by 1;
close `minus`;
end;

--清理环境
drop table minus_test cascade;