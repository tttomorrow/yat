-- @testpoint: degrees函数与其它函数嵌套使用
select degrees(degrees(pi()));
select to_clob((degrees(pi())));