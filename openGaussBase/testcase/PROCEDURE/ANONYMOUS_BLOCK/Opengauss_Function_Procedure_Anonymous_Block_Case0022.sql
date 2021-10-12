-- @testpoint: 验证匿名块内label带引号是否区分大小写  合理报错

declare
  p  varchar2(30);
  n  integer := 37;
begin
    if n = 37 then 
      p := ' is a prime number';
      goto "print_now";
    end if;
  p := ' is not a prime number';
  <<"print_now">>
    raise info ':%',to_char(n) || p;
end;
/

