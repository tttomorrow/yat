--  @testpoint:opengauss关键字table(保留)，作为函数名

--关键字不带引号-失败
drop function if exists table;
create function table(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--关键字带双引号-成功
drop function if exists "table";
create function "table"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function "table";

--关键字带单引号-合理报错
drop function if exists 'table';
create function 'table'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `table`;
create function `table`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/