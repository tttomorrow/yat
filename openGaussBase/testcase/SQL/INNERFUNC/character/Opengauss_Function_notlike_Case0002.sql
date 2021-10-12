-- @testpoint: 函数notlike(x bytea name text, y bytea text)，比较x和y是否不一致，入参为无效值时，合理报错

--参数是英文
select notlike(a,b);
--参数是中文，不带引号
select notlike(哈,哈);
--少参
select notlike(1, );