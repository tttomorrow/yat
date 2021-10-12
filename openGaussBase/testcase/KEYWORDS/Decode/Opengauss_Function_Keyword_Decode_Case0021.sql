--  @testpoint:opengauss关键字decode(非保留)，作为函数名

--关键字不带引号-失败（不可以是函数名）

create or replace function decode(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/

--关键字带双引号-成功（加双引号强制使用关键字）

create function "decode"(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
drop function "decode"(i integer);
--关键字带单引号-合理报错
drop function if exists 'decode';
create function 'decode'(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/
--关键字带反引号-合理报错
drop function if exists `decode`;
create function `decode`(i integer)
returns integer
as $$
begin
    return i+1;
end;
$$ language plpgsql;
/