-- @testpoint: 参数为空，null，空格，合理报错
SELECT btrim(null);
select btrim('');
select btrim(' ');
select btrim();
