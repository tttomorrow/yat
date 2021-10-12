--  @testpoint:opengauss关键字Analyze(保留)，作为游标名

--前置条件
drop table if exists Analyze_test cascade;
create table Analyze_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor Analyze for select * from Analyze_test order by 1;
close Analyze;
end;

--关键字带双引号-成功
start transaction;
cursor "Analyze" for select * from Analyze_test order by 1;
close "Analyze";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'Analyze' for select * from Analyze_test order by 1;
close 'Analyze';
end;

--关键字带反引号-合理报错
start transaction;
cursor `Analyze` for select * from Analyze_test order by 1;
close `Analyze`;
end;

--清理环境
drop table Analyze_test cascade;