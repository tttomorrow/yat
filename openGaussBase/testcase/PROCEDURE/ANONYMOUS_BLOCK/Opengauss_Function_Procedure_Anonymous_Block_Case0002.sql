-- @testpoint: 验证匿名块内变量是否区分大小写

declare
	b number;
begin
	b := 999;
	raise info'B:%',B;
end;
/
